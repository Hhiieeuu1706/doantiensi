from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import csv,json,time

@dataclass
class BMSCycleFrame:
    device_id:str;cycle:int;capacity_ah:float;soh:float;duration_s:float;energy_wh:float;throughput_ah:float
    temperature_mean_c:float;temperature_max_c:float;temperature_rise_c:float;voltage_mean_v:float;voltage_drop_v:float;current_mean_a:float;current_std_a:float
    def to_model_features(self):
        return {"capacity_ah":self.capacity_ah,"soh_initial":self.soh,"duration_s":self.duration_s,"energy_throughput_wh":self.energy_wh,"charge_throughput_ah":self.throughput_ah,"temperature_c_mean":self.temperature_mean_c,"temperature_c_max":self.temperature_max_c,"temperature_rise_c":self.temperature_rise_c,"voltage_v_mean":self.voltage_mean_v,"voltage_drop_v":self.voltage_drop_v,"current_a_mean":self.current_mean_a,"current_a_std":self.current_std_a,"discharge_cycle_index":self.cycle}

class CSVReplayAdapter:
    """Hardware-neutral adapter used for logger exports and software HIL."""
    def __init__(self,path,mapping):self.path=Path(path);self.mapping=mapping
    def frames(self):
        with self.path.open(newline="",encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                values={dst:(row[src] if dst=="device_id" else float(row[src])) for dst,src in self.mapping.items()}
                values["cycle"]=int(values["cycle"]);yield BMSCycleFrame(**values)

class CANAdapterContract:
    """Interface contract. A real implementation requires user-supplied DBC, channel and bitrate."""
    def __init__(self,dbc_path=None,channel=None,bitrate=None):self.dbc_path=dbc_path;self.channel=channel;self.bitrate=bitrate
    def validate_configuration(self):
        missing=[k for k,v in {"dbc_path":self.dbc_path,"channel":self.channel,"bitrate":self.bitrate}.items() if v in (None,"")]
        if missing:raise RuntimeError(f"CAN hardware configuration missing: {missing}")
    def frames(self):
        self.validate_configuration();raise NotImplementedError("Install/configure a CAN backend only after DBC and hardware are supplied")

def load_mapping(path):return json.loads(Path(path).read_text(encoding="utf-8"))
