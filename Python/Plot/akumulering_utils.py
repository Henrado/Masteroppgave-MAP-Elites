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
    t = np.arange(1,experiments[0]["data"][0].shape[0]+1)*scale
    #plt.style.use('default')
    #plt.style.use('seaborn')
    #print(plt.style.library['seaborn'])
    fig, ax = plt.subplots(figsize=(5.5, 4))
    all_means = []

    for dic in experiments:
        arr = dic["data"]
        # Nsteps length arrays empirical means and standard deviations of both
        # populations over time
        mu1 = arr.mean(axis=0)
        sigma1 = arr.std(axis=0)

        # plot it!
        ax.plot(t, mu1, lw=1, label=dic["label"])
        ax.fill_between(t, mu1+sigma1, mu1-sigma1, alpha=0.5)
        #ax.plot(t, mu1, lw=2, label=dic["label"], color=dic["color"])
        #ax.fill_between(t, mu1+sigma1, mu1-sigma1, facecolor=dic["color"], alpha=0.5)
        print(dic["label"], round(mu1[-1], 1))
        all_means.append(mu1[-1])
    print("All means:", round(np.mean(all_means), 1), "\n")
    ax.set_title(title)
    ax.legend(loc='upper left', fontsize=4)
    ax.set_xlabel(xlabel, fontdict=dict(fontsize=12))
    ax.set_ylabel(ylabel, fontdict=dict(fontsize=12))
    ax.grid()
    fig.autofmt_xdate()
    plt.tight_layout()
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
        plot_std_line(experiments, scale=algo_iterations,title=title, output_filename=output_filename, xlabel="Evalueringer", ylabel="QD score")
    else:
        plot_std_line(experiments, title=title, output_filename=output_filename, xlabel="Evalueringer", ylabel="QD score")
    pass

def do_it_all_varShow():
    pass


def do_it_all_boxsplot(experiments: list,filename:str, key:str, key_gruppe:str, key_type, title:str="", output_filename=None):
    #sns.set_theme("paper", style="white")
    for dic in experiments:
        path = dic["path"]
        dataframes, config = get_all_dataframes(path, filename=filename)
        dic["data"] = dataframe2numpy(dataframes, key=key)[:,-1] # type: ignore

    df = pd.DataFrame(columns = ['gruppe', 'type', 'verdier'], dtype="object")
    for dic in experiments:
        en = pd.DataFrame({"gruppe": dic[key_gruppe], "type":dic[key_type], "verdier": dic["data"]}, dtype="object")
        df = pd.concat([df, en], ignore_index = True)
    fig, ax = plt.subplots(figsize=(5.5, 4))

    """ sns.violinplot(ax = ax,
                data = df,
                x = 'gruppe',
                y = 'verdier',
                hue = 'type',
                split = False,
                inner_kws=dict(box_width=3)) """
    sns.boxplot(ax= ax,
                data=df,
                x="gruppe",
                y="verdier",
                hue="type")
    ax.set_title(title)
    ax.legend(title=key_type, fontsize='small')

        # adding horizontal grid lines
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    ax.set_xlabel('', fontdict=dict(fontsize=0))
    ax.set_ylabel('QD score', fontdict=dict(fontsize=12))
    fig.autofmt_xdate()
    plt.tight_layout()
    if output_filename is not None:
        fig.savefig(output_filename)
        plt.close(fig)
    else:
        plt.show()
    pass


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


def do_it_all_grid_per_ex(ex_lost_dict, performance:bool, activity:bool):
    for i in ex_lost_dict:
        filname = "grid.quality_array.csv"
        path = i["path"]
        output_filename = i["filname"] + "_performancesGrid_mean.pdf"
        if performance:
            do_it_all_grid(path, filname, output_filename, True, "mean")

        filname = "grid.activity_per_bin.csv"
        output_filename = i["filname"] + "_grid.activity_per_bin_mean.pdf"
        if activity:
            do_it_all_grid(path, filname, output_filename, False, "mean")
        plt.close()