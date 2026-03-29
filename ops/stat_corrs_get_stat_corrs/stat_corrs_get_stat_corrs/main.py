import os
import json
from pathlib import Path

RUN_NUM = int(os.getenv("RUN_NUM"))
HOME = os.getenv("EC_HOME")

map_vars_file_path = f"{HOME}/map_vars_file/{RUN_NUM}.json"

def load_var_and_data(data_path):
    with open(data_path, "r") as input_data:
        data = json.load(input_data)
        return data["value"]
    
def dump_var_and_data(path, value):
    with open(path, "w") as f:
        json.dump({"value": value}, f)

map_vars_path = load_var_and_data(map_vars_file_path)

map_vars = {}
with open(map_vars_path) as f:
    map_vars = json.load(f)

def get_var_path(map_name):
    global map_vars
    return  f"{HOME}/{map_vars.get(map_name, map_name)}/{RUN_NUM}.json"

def get_obj_path(map_name):
    global map_vars
    return  f"{HOME}/{map_vars.get(map_name, map_name)}/{map_name}.json"

from msm_lib import load_obj, dump_obj
from msm_lib.stat_cors import StatCorsProcessor

traces = load_obj(load_var_and_data(get_var_path("get_stat_corrs__traces_path")))
region = load_obj(load_var_and_data(get_var_path("get_stat_corrs__region_path")))
travel_time = load_obj(load_var_and_data(get_var_path("get_stat_corrs__travel_time_path")))

window_size = load_var_and_data(get_var_path("get_stat_corrs__window_size"))
amount_iter = load_var_and_data(get_var_path("get_stat_corrs__amount_iter"))
batch_size = load_var_and_data(get_var_path("get_stat_corrs__batch_size"))
time_interval = load_var_and_data(get_var_path("get_stat_corrs__time_interval"))
subtrahend = load_var_and_data(get_var_path("get_stat_corrs__subtrahend"))
source_coords = load_var_and_data(get_var_path("get_stat_corrs__source_coords"))

traces = StatCorsProcessor.get_stats(
    traces, 
    region, 
    travel_time,
    source_coords,
    time_interval, 
    amount_iter, 
    batch_size, 
    window_size, 
    subtrahend
)

out_obj_path = get_obj_path("get_stat_corrs__out")
out_var_path = get_var_path("get_stat_corrs__out")
dump_obj(traces, Path(out_obj_path))
dump_var_and_data(out_var_path, out_obj_path)