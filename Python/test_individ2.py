from Unity.Unity_evaluator import UnityEvaluator
from Unity.fitness_funtions import basicFitness, circleFitness
from EA.Individual import *
from EA.Controllers import *
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
import pandas as pd
from ast import literal_eval


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

def get_all_dataframes(path:str, filename:str, parse:bool=False):
    config = yaml.safe_load(open(os.path.join(path, "conf.yaml")))

    arrDataframes = None
    columns = pd.read_csv(os.path.join(path, filename), index_col=0).columns

    if parse:
        arrDataframes = pd.read_csv(os.path.join(path, filename), index_col=0, converters={col:literal_eval for col in columns})
    else:
        arrDataframes = pd.read_csv(os.path.join(path, filename), index_col=0)
    return arrDataframes, config

directory = "../../resultater2/G_S_B_exLimit/1"

d, config = get_all_dataframes(directory, "grid.solutions.csv", parse=True)

arr2 = d.to_numpy()

shape = find_value_from_key(config["containers"], "shape")

# Loads type of individ, controller and fitnessfunction from config
assert "individ" in config["Unity"], f"Please specify configuration entry 'individ'."
conf_individ = config["Unity"]["individ"]
if conf_individ == "Individual_twoLock":
    individ = Individual_twoLock
elif conf_individ == "Individual_zeroLocked":
    individ = Individual_zeroLocked
elif conf_individ == "Individual_globalLock":
    individ = Individual_globalLock
else:
    individ = None
    raise NotImplementedError

assert "controller" in config["Unity"], f"Please specify configuration entry 'controller'."
conf_controller = config["Unity"]["controller"]
if conf_controller == "SineController":
    controller = SineController
elif conf_controller == "SineControllerUfq":
    controller = SineControllerUfq
elif conf_controller == "TanhController":
    controller = TanhController
elif conf_controller == "TanhControllerWOff":
    controller = TanhControllerWOff
elif conf_controller == "TanhControllerWOffFq":
    controller = TanhControllerWOffFq
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


print("\n"*10)
test = (18, 10)
test = (9, 17) #Ikke veldig bra med G_S_B
x = test[0]
y = test[1]
ind = arr2[x][y]
genom = ind[0]["genom"]
fitnessfunction = basicFitness
individ.get_dimension_count(controller) # type: ignore
#ind = np.array([1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0])
print("Directory:", directory)
print("X:", x, "Y:", y)
print("Genom", genom)
print("\n")

try:
    # Create the channel
    if "Qutee" in config:
        qutee_config = config["Qutee"]
        qutee_config["CubeCount"] = 0
    else:
        qutee_config = None 
    print(qutee_config)
    #qutee_config = None
    # Lager evaluator:
    env = UnityEvaluator(1000, qutee_config=qutee_config, editor_mode=True, headless=False, worker_id=0, individ=individ, controller=controller, fitnessfunction=fitnessfunction, time_scale=1)
    
    for i in range(10):
        svar = env.evaluate(genom, False)
        print("Skulle:", (ind[0]["fitness"], ind[0]["features"]))
        print("Endte :",svar)
        print("Diff:", ind[0]["fitness"]-svar[0][0], (ind[0]["features"][0]-svar[1][0], ind[0]["features"][1]-svar[1][1]))
    pass

finally:
    env.close() # type: ignore
    pass