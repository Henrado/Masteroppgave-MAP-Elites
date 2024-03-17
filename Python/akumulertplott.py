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
from ast import literal_eval


def get_all_dataframes(path:str, filename:str, parse:bool=False):
    dir_list = [f.path for f in os.scandir(path) if f.is_dir()]
    config = yaml.safe_load(open(os.path.join(dir_list[0], "conf.yaml")))

    arrDataframes = np.empty(shape=(len(dir_list)), dtype=pd.DataFrame)
    columns = pd.read_csv(os.path.join(dir_list[0], filename), index_col=0).columns

    if parse:
        for i, v in enumerate(dir_list):
            lest = pd.read_csv(os.path.join(v, filename), index_col=0, converters={col:literal_eval for col in columns})
            arrDataframes[i] = lest
    else:
        for i, v in enumerate(dir_list):
            lest = pd.read_csv(os.path.join(v, filename), index_col=0)
            arrDataframes[i] = lest
    print("Kolonnene man kan velge er:", list(arrDataframes[0].columns))
    return arrDataframes, config

def dataframe2numpy(dataframes:np.ndarray, key:str="", dtype=None):
    if key == "":
        arr2 = np.empty(shape=(len(dataframes),dataframes[0].shape[0], dataframes[0].shape[1]), dtype=dtype)
        for i, dataframe in enumerate(dataframes):
            arr2[i] = dataframe.to_numpy()
    else:
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

def do_it_all_stdline(experiments: list,filename:str, key:str, title:str="", output_filename=None, scale=False):
    config = {}
    for dic in experiments:
        path = dic["path"]
        dataframes, config = get_all_dataframes(path, filename=filename)
        dic["data"] = dataframe2numpy(dataframes, key)

    if scale:
        algo_config = config["algorithms"][config["algorithms"]["algoTotal"]["algorithms"][0]]
        algo_iterations = int(np.rint(algo_config["budget"]/algo_config["batch_size"]))
        plot_std_line(experiments, scale=algo_iterations,title=title, output_filename=output_filename)
    else:
        plot_std_line(experiments, title=title, output_filename=output_filename)
    pass

def do_it_all_varShow():
    pass
#container_shape = config["containers"][config["algorithms"]["container"]]["shape"]

determ = [
    {"path": "../../Determ/T_S_B_exLimit", "label": "T_S_B_exLimit", "color": "black"},
    {"path": "../../Determ/Z_S_B_exLimit", "label": "Z_S_B_exLimit", "color": "grey"},
    {"path": "../../Determ/G_S_B_exLimit", "label": "G_S_B_exLimit", "color": "magenta"},

    {"path": "../../Determ/T_SUfq_B_exLimit", "label": "T_SUfq_B_exLimit", "color": "red"},
    {"path": "../../Determ/Z_SUfq_B_exLimit", "label": "Z_SUfq_B_exLimit", "color": "lightcoral"},
    {"path": "../../Determ/G_SUfq_B_exLimit", "label": "G_SUfq_B_exLimit", "color": "peru"},

    {"path": "../../Determ/T_T_B_exLimit", "label": "T_T_B_exLimit", "color": "royalblue"},
    {"path": "../../Determ/Z_T_B_exLimit", "label": "Z_T_B_exLimit", "color": "navy"},
    {"path": "../../Determ/G_T_B_exLimit", "label": "G_T_B_exLimit", "color": "indigo"},

    {"path": "../../Determ/T_TWoff_B_exLimit", "label": "T_TWoff_B_exLimit", "color": "gold"},
    {"path": "../../Determ/Z_TWoff_B_exLimit", "label": "Z_TWoff_B_exLimit", "color": "orange"},
    {"path": "../../Determ/G_TWoff_B_exLimit", "label": "G_TWoff_B_exLimit", "color": "tan"},

    {"path": "../../Determ/T_TWoffFq_B_exLimit", "label": "T_TWoffFq_B_exLimit", "color": "forestgreen"},
    {"path": "../../Determ/Z_TWoffFq_B_exLimit", "label": "Z_TWoffFq_B_exLimit", "color": "lime"},
    {"path": "../../Determ/G_TWoffFq_B_exLimit", "label": "G_TWoffFq_B_exLimit", "color": "palegreen"}
]

miljo = [
    {"path": "../../Miljo/Z_TWoff_B_CS0", "label": "CubeSize=0", "color": "lime"},
    {"path": "../../Miljo/Z_TWoff_B_CS1", "label": "CubeSize=1", "color": "magenta"},
    {"path": "../../Miljo/Z_TWoff_B_CS2", "label": "CubeSize=2", "color": "red"},
    {"path": "../../Miljo/Z_TWoff_B_CS5", "label": "CubeSize=5", "color": "navy"},
    {"path": "../../Miljo/Z_TWoff_B_HCS1", "label": "CubeSize=1 Half", "color": "gold"},
    {"path": "../../Miljo/Z_TWoff_B_HCS2", "label": "CubeSize=2 Half", "color": "forestgreen"},
    {"path": "../../Miljo/Z_TWoff_B_HCS5", "label": "CubeSize=5 Half", "color": "black"}
]
ex_lost_dict = determ
do_it_all_stdline(ex_lost_dict, "iterations.csv", "qd_score", title="QD_score", scale=True)
do_it_all_stdline(ex_lost_dict, "evals.csv", "cont_size", title="Konteiner fylt")
def do_it_all_grid(path:str, filename:str, output_filename:str, quality_array:bool, type_operation:str, scale:float=1):
    d, config = get_all_dataframes(path, filename=filename)
    arr2 = dataframe2numpy(d)

    if type_operation == "max":
        data = np.nanmax(arr2, axis=0)
    elif type_operation == "mean":
        data = np.nanmean(arr2, axis=0)
    elif type_operation == "median":
        data = np.nanmedian(arr2, axis=0)
    elif type_operation == "min":
        data = np.nanmin(arr2, axis=0)
    elif type_operation == "sum":
        data = np.nansum(arr2, axis=0)
    elif type_operation == "std":
        data = np.nanstd(arr2, axis=0)
    else:
        raise ValueError("Invalid type_operation type. Expected one of: [max, min, mean, median, sum, std]")
    
    if not quality_array:
        data = data*scale
        data = data.astype(int)
    max_activity = np.max(data)
    features_domain = config["containers"][config["algorithms"]["container"]]["features_domain"]
    fitness_domain = config["containers"][config["algorithms"]["container"]]["fitness_domain"]
    cmap_perf = "inferno"
    if quality_array:
        plots.plotGridSubplots(data, os.path.join(path, output_filename), plt.get_cmap(cmap_perf), features_domain, fitness_domain[0], nbTicks=None) # type: ignore
    else:
        plots.plotGridSubplots(data, os.path.join(path, output_filename), plt.get_cmap("Reds", max_activity), features_domain, [0, max_activity], nbTicks=None) # type: ignore


path = "../../resultater2/G_S_B_exLimit"
path = "../../resultater2/Z_S_B_exLimit"
filname = "grid.quality_array.csv"
output_filename = "performancesGrid.svg"
#do_it_all_grid(path, filname, output_filename, True, "mean")

filname = "grid.activity_per_bin.csv"
output_filename = "grid.activity_per_bin.svg"
#do_it_all_grid(path, filname, output_filename, False, "max")

""" d, conf = get_all_dataframes(path, "grid.solutions.csv", parse=True)
arr2 = dataframe2numpy(d, dtype=object)

a = np.empty(shape=arr2.shape)
for i in range(arr2.shape[0]):
    for j in range(arr2.shape[1]):
        for k in range(arr2.shape[2]):
            svar = []
            for liste in (arr2[i][j][k]):
                svar.append(liste["genom"][0])
            if len(svar)>0:
                a[i][j][k] = np.nanmax(svar)
b = a[:][9][:] """