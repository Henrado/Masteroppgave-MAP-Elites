from Unity.Unity_evaluator import UnityEvaluator
from Unity.fitness_funtions import basicFitness, circleFitness
from EA.Individual import *
from EA.Controllers import *
from utils.utils import *
from utils.UI import *
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

directory = "../../Determ/Z_T_B_exLimit/1"

d, config = get_one_dataframes(directory, "grid.solutions.csv", parse=True)

arr2 = d.to_numpy()

shape = find_value_from_key(config["containers"], "shape")

individ = get_individ(config=config)
controller = get_controller(config=config)
fitnessfunction = get_individ(config=config)
individ.get_dimension_count(controller) # type: ignore

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
    ui = UI(shape=shape, solutions=arr2)
    for t in range(10000):
        ui.run()
        x,y = ui.get_solution()
        genom = arr2[x][y][0]["genom"]
        individ2 = individ(genom, controller) # type: ignore
        action = individ2.get_actions(t*DELTA_TIME)
        env.send_comand(action)
    pass

finally:
    env.close() # type: ignore
    pass