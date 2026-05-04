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
    return  f"{HOME}/{map_vars.get(map_name, map_name)}/{sgy_name}.json"


from msm_lib import load_obj, dump_obj
from msm_lib.max import MaxProcessor


cube_path_list = load_var_and_data(get_var_path("get_maxes__cube_path"))
detect_function_path_list = load_var_and_data(get_var_path("get_maxes__detect_function_path"))
region_path = load_var_and_data(get_var_path("get_maxes__region_path"))
out_obj_path_list = []
out_var_path = get_var_path("get_maxes__out")

region = load_obj(region_path)
for i in range(len(cube_path_list)):
    try:
        cube_path = Path(cube_path_list[i])
        detect_function_path = Path(detect_function_path_list[i])

        cube = load_obj(cube_path)
        df = load_obj(detect_function_path)
        maxes = MaxProcessor.find_maxes(df, cube, region)
        out_obj_path = get_obj_path("get_maxes__out", cube_path.stem)
        dump_obj(maxes, Path(out_obj_path))
        out_obj_path_list.append(out_obj_path)
    except Exception as e:
        print(e)

dump_var_and_data(out_var_path, out_obj_path_list)

