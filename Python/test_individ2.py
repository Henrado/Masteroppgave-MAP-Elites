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


#directory = "../../Master_Resultater/Determ/G_T_B_exLimit/1"
#directory = "result/time_scale1"


directory = "../../timescale/timescale/kontrollers_timescale/G_S_B_exLimit/102"
directory = "../../timescale/timescale/kontrollers_timescale/G_SUfq_B_exLimit/341"
directory = "../../timescale/timescale/kontrollers_timescale/G_T_B_exLimit/121"
directory = "../../timescale/timescale/kontrollers_timescale/G_TWoff_B_exLimit/363"
directory = "../../timescale/timescale/kontrollers_timescale/G_TWoffFq_B_exLimit/326"

directory = "../../timescale/timescale/kontrollers_timescale/T_S_B_exLimit/155"
directory = "../../timescale/timescale/kontrollers_timescale/T_SUfq_B_exLimit/280"
directory = "../../timescale/timescale/kontrollers_timescale/T_T_B_exLimit/281"
directory = "../../timescale/timescale/kontrollers_timescale/T_TWoff_B_exLimit/301"
directory = "../../timescale/timescale/kontrollers_timescale/T_TWoffFq_B_exLimit/123"

directory = "../../timescale/timescale/kontrollers_timescale/Z_S_B_exLimit/4"
directory = "../../timescale/timescale/kontrollers_timescale/Z_SUfq_B_exLimit/21"
directory = "../../timescale/timescale/kontrollers_timescale/Z_T_B_exLimit/42"
directory = "../../timescale/timescale/kontrollers_timescale/Z_TWoff_B_exLimit/61"
directory = "../../timescale/timescale/kontrollers_timescale/Z_TWoffFq_B_exLimit/81"

directory = "../../timescale/timescale/miljo_timescale/Z_TWoff_B_CS0/1"
directory = "../../timescale/timescale/miljo_timescale/Z_TWoff_B_CS1/416"
directory = "../../timescale/timescale/miljo_timescale/Z_TWoff_B_CS2/170"
directory = "../../timescale/timescale/miljo_timescale/Z_TWoff_B_CS5/458"
directory = "../../timescale/timescale/miljo_timescale/Z_TWoff_B_HCS1/583"
directory = "../../timescale/timescale/miljo_timescale/Z_TWoff_B_HCS2/381"
directory = "../../timescale/timescale/miljo_timescale/Z_TWoff_B_HCS5/221"

d, config = get_one_dataframes(directory, "grid.solutions.csv", parse=True)

arr2 = d.to_numpy()

shape = find_value_from_key(config["containers"], "shape")

individ = get_individ(config=config)
controller = get_controller(config=config)
fitnessfunction = get_fitnessfunction(config=config)


print("\n"*10)
test = (18, 10)
test = (10, 16) #Ikke veldig bra med G_S_B
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
        qutee_config["CubeCount"] = 0
    else:
        qutee_config = None 
    print(qutee_config)
    #qutee_config = None
    # Lager evaluator:
    env = UnityEvaluator(1000, qutee_config=qutee_config, editor_mode=False, headless=False, worker_id=0, individ=individ, controller=controller, fitnessfunction=fitnessfunction, time_scale=1)
    
    a=[]
    b=[]
    c=[]

    for i in range(1):
        csvPath = str(i) + "_gang.csv"
        svar = env.evaluate(genom, csvPath=None, realRobot=True)
        print("Skulle:", (ind[0]["fitness"], ind[0]["features"]))
        print("Endte :",svar)
        diff = np.interp(ind[0]["fitness"]-svar[0][0], [-1, 1], [-180, 180])
        print("Diff:", diff , (ind[0]["features"][0]-svar[1][0], ind[0]["features"][1]-svar[1][1]))
        if round(diff[0], 2) == 0:
            a.append(i)
        else:
            c.append([i, diff[0]])
    print("a",len(a), a)
    print("b",len(b), b)
    print("c",len(c), c)
    pass

finally:
    env.close() # type: ignore
    pass