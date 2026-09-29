from __future__ import annotations
import argparse, json, time, threading, pickle
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import numpy as np
import pandas as pd
import torch

import run_deep_sequence_models as deep
from protocol_v3 import PROTOCOL_ID

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT / "outputs" / "models" / "tcn_online_v1"
DASHBOARD = ROOT / "dashboard"
TABLES = ROOT / "outputs" / "tables"
LOGS = ROOT / "outputs" / "online_service"
LOGS.mkdir(parents=True, exist_ok=True)


class OnlineEstimator:
    def __init__(self):
        self.lock = threading.Lock(); self.buffers = defaultdict(lambda: deque(maxlen=20)); self.history = defaultdict(list); self.idempotency={}
        self.models, self.meta = [], None
        for path in sorted(MODEL_DIR.glob("tcn_seed_*.pt")):
            ck = torch.load(path, map_location="cpu", weights_only=False)
            if self.meta is None: self.meta = ck
            model = deep.TCN(len(ck["features"])+1).cpu(); model.load_state_dict(ck["state_dict"]); model.eval(); self.models.append(model)
        if not self.models: raise FileNotFoundError(f"No TCN artifacts in {MODEL_DIR}")
        self.features = self.meta["features"]; self.length = int(self.meta["sequence_length"])
        self.mean = np.asarray(self.meta["scaler_mean"], float); self.scale = np.asarray(self.meta["scaler_scale"], float)
        self.rul_scale = float(self.meta["rul_scale_cycles"]); self.expansion = float(self.meta["conformal_expansion_cycles"])
        self.replay = pd.read_csv(TABLES / "discharge_cycles_features_labels.csv")
        self.partial_models={}
        for frac in (10,20):
            path=ROOT/"outputs"/"models"/"partial_rul_v1"/f"partial_{frac:02d}pct.pkl"
            if path.exists():
                with path.open("rb") as f:self.partial_models[frac/100]=pickle.load(f)

    def validate(self, payload):
        missing = [f for f in self.features if f not in payload]
        if missing: return False, f"missing fields: {missing}"
        bounds = {"capacity_ah": (0, 10), "soh_initial": (0, 1.5), "duration_s": (0, 100000),
                  "temperature_c_mean": (-30, 100), "temperature_c_max": (-30, 120),
                  "voltage_v_mean": (0, 6), "current_a_mean": (-20, 20), "discharge_cycle_index": (1, 100000)}
        for f, (lo, hi) in bounds.items():
            v = float(payload[f])
            if not np.isfinite(v) or not lo <= v <= hi: return False, f"{f}={v} outside [{lo},{hi}]"
        return True, "ok"

    def predict(self, device_id, payload, request_id=None):
        if request_id and request_id in self.idempotency:return self.idempotency[request_id]
        ok, msg = self.validate(payload)
        if not ok: raise ValueError(msg)
        started = time.perf_counter()
        row = np.asarray([float(payload[f]) for f in self.features], float)
        with self.lock:
            last_cycle=int(self.buffers[device_id][-1][self.features.index("discharge_cycle_index")]) if self.buffers[device_id] else 0
            current_cycle=int(payload["discharge_cycle_index"])
            if current_cycle<=last_cycle:raise ValueError(f"duplicate_or_out_of_order_cycle: current={current_cycle}, last={last_cycle}")
            cycle_gap=max(0,current_cycle-last_cycle-1) if last_cycle else 0
            self.buffers[device_id].append(row); seq = list(self.buffers[device_id])
        x = np.vstack(seq); pad = self.length-len(x); mask = np.r_[np.zeros(pad), np.ones(len(x))][:, None]
        x = np.vstack([np.zeros((pad, len(self.features))), x]); z = np.zeros_like(x); valid = mask[:, 0] > 0
        z[valid] = (x[valid]-self.mean)/np.where(self.scale == 0, 1, self.scale)
        tensor = torch.tensor(np.hstack([z, mask])[None], dtype=torch.float32)
        with torch.no_grad(): preds = np.asarray([m(tensor).item()*self.rul_scale for m in self.models])
        pred = max(0.0, float(preds.mean())); lo = max(0.0, float(np.quantile(preds, .05))-self.expansion)
        hi = float(np.quantile(preds, .95))+self.expansion; soh = float(payload["soh_initial"])
        risk = "critical" if pred <= 10 or soh <= .72 else ("warning" if pred <= 25 or soh <= .80 else "normal")
        drift_score=float(np.nanmax(np.abs((row-self.mean)/np.where(self.scale==0,1,self.scale))));domain="out_of_domain" if drift_score>8 else ("warning" if drift_score>5 else "in_domain")
        result = {"protocol_id": PROTOCOL_ID, "model": "TCN-online-v1-developmental", "device_id": device_id,
                  "cycle": int(payload["discharge_cycle_index"]), "soh": soh, "rul_pred": pred,
                  "rul_low": lo, "rul_high": hi, "interval_status": "developmental_not_cross_domain_calibrated",
                  "risk": risk, "ensemble_std": float(preds.std(ddof=1)), "buffer_cycles": len(seq),"cycle_gap":cycle_gap,"domain_status":domain,"drift_score":drift_score,"prediction_allowed":domain!="out_of_domain",
                  "latency_ms": (time.perf_counter()-started)*1000, "timestamp_unix": time.time()}
        with self.lock:
            self.history[device_id].append(result); self.history[device_id] = self.history[device_id][-500:]
        with (LOGS / "predictions.jsonl").open("a", encoding="utf-8") as f: f.write(json.dumps(result)+"\n")
        if request_id:self.idempotency[request_id]=result
        return result

    def predict_partial(self,device_id,fraction,payload,request_id=None):
        if request_id and request_id in self.idempotency:return self.idempotency[request_id]
        fraction=float(fraction);artifact=self.partial_models.get(fraction)
        if artifact is None:raise ValueError("fraction must be 0.1 or 0.2")
        missing=[f for f in artifact["features"] if f not in payload]
        if missing:raise ValueError(f"missing partial fields: {missing}")
        x=pd.DataFrame([{f:float(payload[f]) for f in artifact["features"]}]);started=time.perf_counter();pipe=artifact["model"];pred=max(0,float(pipe.predict(x)[0]));clean=pipe.named_steps["impute"].transform(x);forest=pipe.named_steps["rf"];trees=np.asarray([t.predict(clean)[0] for t in forest.estimators_]);exp=float(artifact["conformal_expansion"]);lo=max(0,float(np.quantile(trees,.05))-exp);hi=float(np.quantile(trees,.95))+exp
        # RF leaf extrapolation is not reliable; range distance is a conservative drift proxy.
        train_min=np.asarray([t.tree_.threshold[t.tree_.threshold>-2].min(initial=0) for t in forest.estimators_]);spread=float(np.std(trees,ddof=1));domain="warning" if spread>25 else "in_domain"
        result={"protocol_id":artifact["protocol_id"],"model":f"RF-partial-{int(fraction*100)}pct-developmental","mode":"partial_cycle","observed_fraction":fraction,"device_id":device_id,"cycle":int(payload["discharge_cycle_index"]),"rul_pred":pred,"rul_low":lo,"rul_high":hi,"ensemble_std":spread,"domain_status":domain,"drift_score":spread/10,"prediction_allowed":domain!="out_of_domain","risk":"critical" if pred<=10 else ("warning" if pred<=25 else "normal"),"interval_status":"developmental_training_residual_calibration","latency_ms":(time.perf_counter()-started)*1000,"timestamp_unix":time.time()}
        with self.lock:self.history[device_id].append(result);self.history[device_id]=self.history[device_id][-500:]
        if request_id:self.idempotency[request_id]=result
        return result

    def reset(self, device_id):
        with self.lock: self.buffers.pop(device_id, None); self.history.pop(device_id, None)

    def replay_cycle(self, device_id, battery_id, cycle=None):
        b = self.replay[self.replay.battery_id == battery_id].sort_values("discharge_cycle_index")
        if b.empty: raise ValueError(f"unknown battery {battery_id}")
        next_cycle = cycle or (len(self.history[device_id])+1)
        row = b[b.discharge_cycle_index == next_cycle]
        if row.empty: raise ValueError(f"cycle {next_cycle} unavailable for {battery_id}")
        r = row.iloc[0]; payload = {f: float(r[f]) for f in self.features}
        return self.predict(device_id, payload)


EST = OnlineEstimator()


class Handler(BaseHTTPRequestHandler):
    def send_json(self, obj, code=200):
        body = json.dumps(obj, allow_nan=False).encode(); self.send_response(code)
        self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers(); self.wfile.write(body)
    def do_OPTIONS(self):
        self.send_response(204); self.send_header("Access-Control-Allow-Origin", "*"); self.send_header("Access-Control-Allow-Headers", "Content-Type"); self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS"); self.end_headers()
    def do_GET(self):
        p = urlparse(self.path); q = parse_qs(p.query)
        try:
            if p.path == "/api/health": return self.send_json({"status":"ok","models":len(EST.models),"protocol_id":PROTOCOL_ID})
            if p.path == "/api/status": return self.send_json({"devices":{k:(v[-1] if v else None) for k,v in EST.history.items()}})
            if p.path == "/api/history": return self.send_json(EST.history.get(q.get("device_id",["demo"])[0], []))
            path = DASHBOARD / ("index.html" if p.path == "/" else p.path.lstrip("/"))
            if path.exists() and path.is_file():
                body=path.read_bytes(); ctype="text/css" if path.suffix==".css" else ("application/javascript" if path.suffix==".js" else "text/html")
                self.send_response(200); self.send_header("Content-Type",ctype); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body); return
            self.send_json({"error":"not found"},404)
        except Exception as e: self.send_json({"error":str(e)},400)
    def do_POST(self):
        try:
            n=int(self.headers.get("Content-Length","0")); data=json.loads(self.rfile.read(n) or b"{}")
            if self.path in ("/api/cycle","/api/completed-cycle"): return self.send_json(EST.predict(data.get("device_id","demo"),data["features"],data.get("request_id")))
            if self.path == "/api/partial-cycle": return self.send_json(EST.predict_partial(data.get("device_id","demo"),data.get("observed_fraction"),data["features"],data.get("request_id")))
            if self.path == "/api/reset": EST.reset(data.get("device_id","demo")); return self.send_json({"reset":True})
            if self.path == "/api/hil/tick": return self.send_json(EST.replay_cycle(data.get("device_id","hil-demo"),data.get("battery_id","B0005"),data.get("cycle")))
            self.send_json({"error":"not found"},404)
        except Exception as e: self.send_json({"error":str(e)},400)
    def log_message(self, *_): pass


if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--host",default="127.0.0.1"); ap.add_argument("--port",type=int,default=8765); args=ap.parse_args()
    print(f"Battery RUL service: http://{args.host}:{args.port}", flush=True)
    ThreadingHTTPServer((args.host,args.port),Handler).serve_forever()
