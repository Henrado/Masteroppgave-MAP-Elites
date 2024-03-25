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
import pickle


def find_value_from_key(data, key):
    for k, v in data.items():
        if key in data[k]:
            return data[k][key]
    return None

def shortestAngle(from_deg, to_deg):
    diff = from_deg - to_deg
    while ((diff >  180).any()): diff[diff >  180] -= 2*180 # type: ignore
    while ((diff < -180).any()): diff[diff < -180] += 2*180 # type: ignore
    return diff

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

def get_one_dataframes(path:str, filename:str, parse:bool=False):
    config = yaml.safe_load(open(os.path.join(path, "conf.yaml")))

    arrDataframes = None
    columns = pd.read_csv(os.path.join(path, filename), index_col=0).columns

    if parse:
        arrDataframes = pd.read_csv(os.path.join(path, filename), index_col=0, converters={col:literal_eval for col in columns})
    else:
        arrDataframes = pd.read_csv(os.path.join(path, filename), index_col=0)
    return arrDataframes, config

def get_individ(config: dict):
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
    return individ

def get_controller(config: dict):
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
    return controller

def get_fitnessfunction(config: dict):
    assert "fitnessfunction" in config["Unity"], f"Please specify configuration entry 'fitnessfunction'."
    conf_individ = config["Unity"]["fitnessfunction"]
    if conf_individ == "basicFitness":
        fitnessfunction = basicFitness
    elif conf_individ == "circleFitness":
        fitnessfunction = circleFitness
    else:
        fitnessfunction = None
        raise NotImplementedError
    return fitnessfunction

def pickle2json(path):
    # open pickle file
    with open(path, 'rb') as infile:
        obj = pickle.load(infile)

    # convert pickle object to json object
    json_obj = json.loads(json.dumps(obj, default=str))

    # write the json file
    with open(
            os.path.splitext(path)[0] + '.json',
            'w',
            encoding='utf-8'
        ) as outfile:
        json.dump(json_obj, outfile, ensure_ascii=False, indent=4)