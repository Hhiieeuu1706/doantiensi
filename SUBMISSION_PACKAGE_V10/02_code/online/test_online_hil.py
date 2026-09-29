from __future__ import annotations
import json, statistics, time, os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "outputs" / "reports" / "ONLINE_API_HIL_TEST.md"
BASE = os.environ.get("BATTERY_RUL_BASE_URL","http://127.0.0.1:8765")


def get(path):
    return json.loads(urlopen(BASE+path, timeout=10).read())


def post(path, payload):
    req = Request(BASE+path, json.dumps(payload).encode(), {"Content-Type":"application/json"}, method="POST")
    return json.loads(urlopen(req, timeout=20).read())


def main():
    tests=[]; health=get("/api/health"); tests.append(("health",health["status"]=="ok",health))
    post("/api/reset",{"device_id":"hil-benchmark"}); results=[]
    for _ in range(25): results.append(post("/api/hil/tick",{"device_id":"hil-benchmark","battery_id":"B0005"}))
    tests.append(("sequential_cycles",[x["cycle"] for x in results]==list(range(1,26)),"cycles 1..25"))
    tests.append(("state_buffer",results[-1]["buffer_cycles"]==20,results[-1]["buffer_cycles"]))
    tests.append(("physical_intervals",all(x["rul_low"]>=0 and x["rul_low"]<=x["rul_pred"]<=x["rul_high"] for x in results),"25 cases"))
    tests.append(("finite_latency",all(x["latency_ms"]>0 for x in results),"25 cases"))
    history=get("/api/history?device_id=hil-benchmark"); tests.append(("history_endpoint",len(history)==25,len(history)))
    rejected=False
    try: post("/api/cycle",{"device_id":"bad","features":{"capacity_ah":-1}})
    except HTTPError as e: rejected=e.code==400
    tests.append(("invalid_payload_rejected",rejected,"HTTP 400 expected"))
    # Idempotency and ordering.
    partial=pd.read_csv(ROOT/"outputs"/"tables"/"partial_discharge_features.csv");pr=partial[(partial.battery_id=="B0005")&np.isclose(partial.observed_curve_fraction,.1)].iloc[0];base=pd.read_csv(ROOT/"outputs"/"tables"/"discharge_cycles_features_labels.csv");lag=base[(base.battery_id=="B0005")&(base.discharge_cycle_index==int(pr.discharge_cycle_index))].capacity_lag1_ah.iloc[0]
    fields=["discharge_cycle_index","partial_duration_s","partial_energy_wh","partial_throughput_ah","partial_voltage_mean_v","partial_voltage_std_v","partial_voltage_drop_v","partial_current_mean_a","partial_current_std_a","partial_temperature_mean_c","partial_temperature_max_c","partial_temperature_rise_c"]
    feat={f:float(pr[f]) for f in fields};feat["capacity_lag1_ah"]=None if pd.isna(lag) else float(lag)
    # First-cycle lag is unknown; use the first reported capacity as prior BMS estimate for API smoke test.
    if feat["capacity_lag1_ah"] is None:feat["capacity_lag1_ah"]=float(pr.capacity_ah)
    a=post("/api/partial-cycle",{"device_id":"partial-test","observed_fraction":.1,"request_id":"partial-once","features":feat});b=post("/api/partial-cycle",{"device_id":"partial-test","observed_fraction":.1,"request_id":"partial-once","features":feat})
    tests.append(("partial_cycle_endpoint",a["mode"]=="partial_cycle" and a["rul_pred"]>=0,a["rul_pred"]))
    tests.append(("idempotency",a==b,"same response"))
    def one_device(i):return post("/api/hil/tick",{"device_id":f"concurrent-{i}","battery_id":"B0005"})
    with ThreadPoolExecutor(max_workers=8) as ex:concurrent=list(ex.map(one_device,range(12)))
    tests.append(("concurrent_devices",len(concurrent)==12 and all(x["cycle"]==1 for x in concurrent),"12 devices"))
    post("/api/reset",{"device_id":"hil-benchmark"}); tests.append(("reset",len(get("/api/history?device_id=hil-benchmark"))==0,"empty history"))
    lat=[x["latency_ms"] for x in results]
    passed=sum(x[1] for x in tests)
    text=f"# Online API and hardware-in-loop simulation test\n\nPassed **{passed}/{len(tests)}** tests.\n\n- Median inference latency: {statistics.median(lat):.2f} ms\n- P95 latency: {sorted(lat)[int(.95*(len(lat)-1))]:.2f} ms\n- Ensemble models: {health['models']}\n- Replay source: NASA B0005 cycles 1–25\n\n| Test | Passed | Detail |\n|---|---:|---|\n"
    for name,ok,detail in tests:text+=f"| {name} | {ok} | {detail} |\n"
    text+="\nThis is software HIL/replay validation, not electrical hardware or a production BMS certification.\n"
    REPORT.write_text(text,encoding="utf-8");print(json.dumps({"passed":passed,"total":len(tests),"median_latency_ms":statistics.median(lat),"p95_latency_ms":sorted(lat)[int(.95*(len(lat)-1))]},indent=2))
    if passed != len(tests): raise SystemExit(1)


if __name__=="__main__":main()
