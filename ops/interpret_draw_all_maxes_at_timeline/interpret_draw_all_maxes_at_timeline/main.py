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
    return  f"{HOME}/{map_vars.get(map_name, map_name)}"


from msm_lib import load_obj, dump_obj
from msm_lib.result_interpret import Interpretator

maxes_list_path = load_var_and_data(get_var_path("draw_maxes_at_timeline__maxes_list_path"))
out_obj_path = get_obj_path("draw_maxes_at_timeline__chart_maxes_at_timeline")
out_var_path = get_var_path("draw_maxes_at_timeline__chart_maxes_at_timeline")

maxes_list = []

for path in maxes_list_path:
    maxes_list.append(load_obj(path))


Interpretator.draw_maxes_at_timeline(maxes_list,
                         Path(out_obj_path) / "maxes_at_timeline.png")

