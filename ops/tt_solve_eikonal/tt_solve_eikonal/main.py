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
from msm_lib.time_calculation import EikonalSolver

model_path = load_var_and_data(get_var_path("solve_eikonal__model_path"))
source = load_var_and_data(get_var_path("solve_eikonal__source"))
out_var_path = get_var_path("solve_eikonal__out")
out_obj_path = get_obj_path("solve_eikonal__out")

with open(model_path, "r") as f:
    d = json.load(f)
    print(d.keys())

model = load_obj(model_path)

esolve = EikonalSolver.solve(model, source)
dump_obj(esolve, Path(out_obj_path))
dump_var_and_data(out_var_path, out_obj_path)

