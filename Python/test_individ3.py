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

def read_dataframe(path:str, filename:str, parse:bool=False):

    columns = pd.read_csv(os.path.join(path, filename), index_col=0).columns

    if parse:
        arrDataframes = pd.read_csv(os.path.join(path, filename), index_col=0, converters={col:literal_eval for col in columns})
    else:
        arrDataframes = pd.read_csv(os.path.join(path, filename), index_col=0)
    print("Kolonnene man kan velge er:", list(arrDataframes.columns))
    return arrDataframes

individ = Individual_zeroLocked
controller = SineController
fitnessfunction = basicFitness
individ.get_dimension_count(controller) # type: ignore

d = read_dataframe("", "index_0.csv")
d = d.to_numpy()

try:
    # Create the channel
    qutee_config = None 
    #qutee_config = None
    # Lager evaluator:
    env = UnityEvaluator(1000, qutee_config=qutee_config, editor_mode=False, headless=False, worker_id=0, individ=individ, controller=controller, fitnessfunction=fitnessfunction)
        
    svar = env.evaluate2(d)
    print("HER:",svar)
    pass

finally:
    env.close() # type: ignore
    pass