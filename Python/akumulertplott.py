import pandas as pd
import json
import numpy as np
from Plot.plots import min_plots_grid, min_summary
from qdpy import algorithms, containers, plots
from qdpy.base import Summarisable
import os
import numpy as np
import matplotlib.pyplot as plt
from qdpy import containers
from qdpy import algorithms
import json
import pandas as pd
import textwrap
from typing import Optional, Tuple, List, Iterable, Iterator, Any, TypeVar, Generic, Union, Sequence, MutableSet, MutableSequence, Type, Callable, Generator, Mapping, MutableMapping, overload
from qdpy.utils import is_iterable
from functools import reduce
import xarray as xr
import seaborn as sns
import yaml



path = "test/evals.csv"
path = "test/iterations.csv"
path = "test/grid.quality.csv"
path = "test/grid.quality_array.csv"
path = "test/grid.items.csv"
path = "test/grid.nb_items_per_bin.csv"
path = "test/grid.activity_per_bin.csv"
path = "test/grid.features.csv"
path = "test/grid.recentness.csv"
path = "test/grid.solutions.csv"

def get_all_dataframes(path:str, filename:str):
    dir_list = os.listdir(path)
    config = yaml.safe_load(open(os.path.join(path, dir_list[0], "conf.yaml")))

    arrDataframes = np.empty(shape=(len(dir_list)), dtype=pd.DataFrame)

    for i, v in enumerate(dir_list):
        lest = pd.read_csv(os.path.join(path, v, filename), index_col=0)
        arrDataframes[i] = lest
    print("Kolonnene man kan velge er:", list(arrDataframes[0].columns))
    return arrDataframes, config

def dataframe2numpy(dataframes:np.ndarray, key:str):
    arr2 = np.empty(shape=(dataframes.shape[0], dataframes[0].shape[0]))
    for i, v in enumerate(dataframes):
        arr2[i] = v[key]
    return arr2

def plot_std_line(experiments:list, scale:float=1, output_filename=None, title="", xlabel="Evaluations", ylabel=""):
    t = np.arange(experiments[0]["data"][0].shape[0])*scale
    fig, ax = plt.subplots(1)

    for dic in experiments:
        arr = dic["data"]
        # Nsteps length arrays empirical means and standard deviations of both
        # populations over time
        mu1 = arr.mean(axis=0)
        sigma1 = arr.std(axis=0)

        # plot it!
        ax.plot(t, mu1, lw=2, label=dic["label"], color=dic["color"])
        ax.fill_between(t, mu1+sigma1, mu1-sigma1, facecolor=dic["color"], alpha=0.5)
    ax.set_title(title)
    ax.legend(loc='upper left')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    if output_filename is not None:
        fig.savefig(output_filename)
        plt.close(fig)
    else:
        plt.show()

def do_it_all_stdline(experiments: list,filename:str, key:str, output_filename=None, scale=False):
    config = {}
    for dic in experiments:
        path = dic["path"]
        dataframes, config = get_all_dataframes(path, filename=filename)
        dic["data"] = dataframe2numpy(dataframes, key)

    if scale:
        algo_config = config["algorithms"][config["algorithms"]["algoTotal"]["algorithms"][0]]
        algo_iterations = int(np.rint(algo_config["budget"]/algo_config["batch_size"]))
        plot_std_line(experiments, scale=algo_iterations, output_filename=output_filename)
    else:
        plot_std_line(experiments, output_filename=output_filename)
    pass

#container_shape = config["containers"][config["algorithms"]["container"]]["shape"]

ex_lost_dict = [
    {"path": "result/testslurm", "label": "forsøk1", "color": "blue"},
    {"path": "result/testslurm2", "label": "forsøk2", "color": "red"}
]
do_it_all_stdline(ex_lost_dict, "iterations.csv", "max", scale=True)
#do_it_all_stdline(ex_lost_dict, "evals.csv", "cont_size")