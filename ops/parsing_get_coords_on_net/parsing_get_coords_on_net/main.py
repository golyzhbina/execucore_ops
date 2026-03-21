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
from msm_lib.parsing import ReceiverCoordsHandlerNPY

rec_coords_path = load_var_and_data(get_var_path("get_coords_on_net__rec_coords_path"))
region_path = load_var_and_data(get_var_path("get_coords_on_net__region_path"))
out_var_path = get_var_path("get_coords_on_net__out")
out_obj_path = get_obj_path("get_coords_on_net__out")

region = load_obj(region_path)
rec_coords = load_obj(rec_coords_path)

rec_coords_on_net = ReceiverCoordsHandlerNPY.get_coords_on_net(rec_coords, region)
dump_obj(rec_coords_on_net, Path(out_obj_path))
dump_var_and_data(out_var_path, out_obj_path)

