from Unity.Unity_evaluator import UnityEvaluator
from Unity.fitness_funtions import basicFitness, circleFitness
from EA.Individual import Individual_zeroLocked, Individual_twoLock
from EA.Controllers import SineController, TanhController, TanhControllerWOff
import numpy as np
import argparse
from qdpy import algorithms, containers, plots
from qdpy.base import ParallelismManager
import math
import os
import json
import sys
import re
import yaml

def find_value_from_key(data, key):
    for k, v in data.items():
        if key in data[k]:
            return data[k][key]
    return None

def str_to_2Darr(shape, string):

    # Se eksempel på regex: https://regex101.com/r/oqnsHa/1
    # For å slette regex: https://regex101.com/delete/PjW4IlAeGfi95Tnr2pNK0yUVJ9g73nPMCTmx https://regex101.com/delete/1/VpEVefxZk8KL134d2HcI8pvcdWX9T8oyLYdF
    pairs = re.findall(r'\\\"(\[\d*,\s\d*])\\\":.*?((?:\[])|(?:\[\[.*?]]))', string)
    rows, cols = shape
    arr = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(0, len(pairs)):
        a = json.loads(pairs[i][0])
        b = json.loads(pairs[i][1])
        arr[a[0]][a[1]] = b
    return arr


directory = "result/25.12.23/25.12.23_twolock_tanh"
# Retrieve configuration from configFile
config = yaml.safe_load(open(os.path.join(directory, "conf.yaml")))

#open JSON file
with open(os.path.join(directory, "grid.solutions.json"), 'r', encoding='utf-8') as infile:
   json_str = infile.read()

shape = find_value_from_key(config["containers"], "shape")
json_obj = str_to_2Darr((shape[0],shape[1]), json_str) #type: ignore

    # Loads type of individ, controller and fitnessfunction from config
assert "individ" in config["Unity"], f"Please specify configuration entry 'individ'."
conf_individ = config["Unity"]["individ"]
if conf_individ == "Individual_twoLock":
    individ = Individual_twoLock
elif conf_individ == "Individual_zeroLocked":
    individ = Individual_zeroLocked
else:
    individ = None
    raise NotImplementedError

assert "controller" in config["Unity"], f"Please specify configuration entry 'controller'."
conf_controller = config["Unity"]["controller"]
if conf_controller == "SineController":
    controller = SineController
elif conf_controller == "TanhController":
    controller = TanhController
elif conf_controller == "TanhControllerWOff":
    controller = TanhControllerWOff
else:
    controller = None
    raise NotImplementedError

assert "fitnessfunction" in config["Unity"], f"Please specify configuration entry 'fitnessfunction'."
conf_individ = config["Unity"]["fitnessfunction"]
if conf_individ == "basicFitness":
    fitnessfunction = basicFitness
elif conf_individ == "circleFitness":
    fitnessfunction = circleFitness
else:
    fitnessfunction = None
    raise NotImplementedError

x = 17
y = 17
ind = json_obj[x][y][0]
individ.get_dimension_count(controller) # type: ignore
print(ind)

try:
    # Create the channel
    if "Qutee" in config:
        qutee_config = config["Qutee"]
    else:
        qutee_config = None
    # Lager evaluator:
    env = UnityEvaluator(80, qutee_config=qutee_config, editor_mode=False, headless=False, worker_id=0, individ=individ, controller=controller, fitnessfunction=fitnessfunction)
        
    svar = env.evaluate(ind, True)
    print("HER:",svar)
    pass

finally:
    env.close() # type: ignore
    pass