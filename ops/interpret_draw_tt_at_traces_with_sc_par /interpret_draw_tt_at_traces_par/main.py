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


def get_obj_path(map_name, sgy_name):
    global map_vars
    return  f"{HOME}/{map_vars.get(map_name, map_name)}/{sgy_name}"


from msm_lib import load_obj, dump_obj
from msm_lib.result_interpret import Interpretator

maxes_path_list = load_var_and_data(get_var_path("draw_tt_at_traces__maxes_path"))
traces_path_list = load_var_and_data(get_var_path("draw_tt_at_traces__traces_path"))
tt_path = load_var_and_data(get_var_path("draw_tt_at_traces__tt_path"))
region_path = load_var_and_data(get_var_path("draw_tt_at_traces__region_path"))
radius = load_var_and_data(get_var_path("draw_tt_at_traces__radius"))
sc_path = load_var_and_data(get_var_path("draw_tt_at_traces__stat_corrs_path"))

out_var_path = get_var_path("draw_tt_at_traces__out")

tt = load_obj(tt_path)
region = load_obj(region_path)
stat_corrs = load_obj(sc_path)

for i in range(len(maxes_path_list)):
    try:
        maxes_path = Path(maxes_path_list[i])
        traces_path = Path(traces_path_list[i])
        maxes = load_obj(maxes_path)
        traces = load_obj(traces_path)
        out_obj_path = get_obj_path("draw_tt_at_traces__out", maxes_path.stem)
        os.makedirs(out_obj_path, exist_ok=True)
        Interpretator.draw_tt_at_traces(maxes, 
                                        traces, 
                                        tt, 
                                        stat_corrs,
                                        region.amount_x, 
                                        radius, 
                                        out_obj_path)
    except Exception as e:
        print(e)

