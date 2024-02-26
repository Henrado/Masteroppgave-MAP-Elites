from Unity.Unity_evaluator import UnityEvaluator
from Unity.fitness_funtions import basicFitness, circleFitness
from EA.Individual import *
from EA.Controllers import *
from utils.utils import *
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


directory = "../../Determ/G_S_B_exLimit/1"

d, config = get_one_dataframes(directory, "grid.solutions.csv", parse=True)

arr2 = d.to_numpy()

shape = find_value_from_key(config["containers"], "shape")

individ = get_individ(config=config)
controller = get_controller(config=config)
fitnessfunction = get_individ(config=config)


print("\n"*10)
test = (18, 10)
test = (19, 8) #Ikke veldig bra med G_S_B
x = test[0]
y = test[1]
ind = arr2[x][y]
genom = ind[0]["genom"]
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
        #qutee_config["CubeCount"] = 0
    else:
        qutee_config = None 
    print(qutee_config)
    #qutee_config = None
    # Lager evaluator:
    env = UnityEvaluator(1000, qutee_config=qutee_config, editor_mode=False, headless=False, worker_id=0, individ=individ, controller=controller, fitnessfunction=fitnessfunction, time_scale=1)
    
    for i in range(2):
        svar = env.evaluate(genom, False)
        print("Skulle:", (ind[0]["fitness"], ind[0]["features"]))
        print("Endte :",svar)
        diff = np.interp(ind[0]["fitness"]-svar[0][0], [-1, 1], [-180, 180])
        print("Diff:", diff , (ind[0]["features"][0]-svar[1][0], ind[0]["features"][1]-svar[1][1]))
    pass

finally:
    env.close() # type: ignore
    pass