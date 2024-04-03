from Unity.Unity_evaluator import UnityEvaluator
from Unity.fitness_funtions import basicFitness, circleFitness
from EA.Individual import *
from EA.Controllers import *
from utils.utils import *
from utils.UI import *
from utils.Plan import *
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
import pygame
from pygame.locals import *

directory = "../../Master_Resultater/Determ/G_T_B_exLimit/1"

d, config = get_one_dataframes(directory, "grid.solutions.csv", parse=True)

arr2 = d.to_numpy()

shape = find_value_from_key(config["containers"], "shape")

individ = get_individ(config=config)
controller = get_controller(config=config)
fitnessfunction = get_fitnessfunction(config=config)
individ.get_dimension_count(controller) # type: ignore

if True:
    p = [
        {"tid": 500, "x": 10, "y":10},
        {"tid": 500, "x": 16, "y":10},
        {"tid": 500, "x": 3, "y":16},
        {"tid": 500, "x": 7, "y":7},
        {"tid": 500, "x": 12, "y":14},
        {"tid": 500, "x": 13, "y":3},
        {"tid": 1, "x": 7, "y":7}
    ]
    genomGenerator = Plan(p)
else:
    genomGenerator = UI(shape=shape, solutions=arr2)
    genomGenerator.run()
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
    env = UnityEvaluator(10000, qutee_config=qutee_config, editor_mode=False, headless=False, worker_id=0, individ=individ, controller=controller, fitnessfunction=fitnessfunction, time_scale=1)
    
    DELTA_TIME = 0.01
    end_position = np.zeros((1,3))
    end_rotation = 0
    last_rotation = 0 # Denne kan ikke være np.zeros((1,3)) siden da vil last_rotation bli = [[x,y,z]] ikke [x,y,z]
    last_ind = 0
    if_pause = True

    env.configRobot(True)

    df = pd.DataFrame(columns=["x", "z", "y_rot"])
    for t in range(10000):
        x,y,ind = genomGenerator.get_solution(t) # type: ignore
        if x==None or y==None:
            break
        genom = arr2[x][y][0]["genom"]
        individ2 = individ(genom, controller) # type: ignore
        action = individ2.get_actions(t*DELTA_TIME)
        obs = env.send_comand(action)
        
        end_position = obs[0][0][:3] # Henter observasjonene til agent 0 
        end_rotation += shortestAngle(obs[0][0][3:6],last_rotation)
        last_rotation = obs[0][0][3:6]

        end_x = end_position[0]
        end_z = end_position[2]
        end_yrot = end_rotation[1] # type: ignore
        df.loc[t] = {"x":end_x, "z": end_z, "y_rot": end_yrot}
        if ind != last_ind and if_pause:
            last_ind = ind
            fitness = env.fitnessfunction(end_x, end_z, end_yrot) # type: ignore 
            fitness = np.interp(fitness, [-1, 1], [-180, 180])
            print((fitness,), (end_x, end_z))
            #input("Trykk enter for å fortsette")
    pass
finally:
    env.configRobot(False)
    print(df)
    df.to_csv("Z_T_B_exLimit.csv")
    env.close() # type: ignore
    pass