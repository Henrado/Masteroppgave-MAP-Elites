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


def json_dumps_tuple_keys(mapping):
    string_keys = {json.dumps(k): v for k, v in mapping.items()}
    return json.dumps(string_keys)

def json_loads_tuple_keys(string):
    mapping = json.loads(string)
    return {tuple(json.loads(k)): v for k, v in mapping.items()}

def dict_to_2Darray(dict:dict, shape:tuple, feature:bool=False, individ:bool=False):
    arr = np.empty(shape, dtype=object)
    for key, value in dict.items():
        #print(key[0])
        if feature:
            value = [i.getValues() for i in value]
        elif individ:
            indi = []
            for i in value:
                dic = {
                    "name": i.name,
                    "genom": list(i),
                    "fitness": i.fitness.getValues(),
                    "features": i.features.getValues()
                    }
                indi.append(dic)
            value = indi
        arr[key[0]][key[1]] = value
    return arr

def min_summary(algo, max_depth = None, max_entry_length = None) -> str:
        """Return a summary description of the class.
        The summarised information is provided by the `self.__get_summary_state__` method.

        Parameters
        ----------
        :param max_depth: Optional[int]
            The maximal recursion depth allowed. Used to summarise attributes of `self` that are also Summarisable.
            If the maximal recursion depth is reached, the attribute is only described with a reduced representation (`repr(attribute)`).
            If `max_depth` is set to None, there are no recursion limit.
        :param max_entry_length: Optional[int]
            If `max_entry_length` is not None, the description of a non-Summarisable entry exceeding `max_entry_length`
            is cropped to this limit.
        """
        res: str = f"Summary {algo.__class__.__name__}:\n"
        subs_max_depth = max_depth - 1 if max_depth is not None else None
        summary_state = algo.__get_summary_state__()
        for i, k in enumerate(summary_state.keys()):
            v = summary_state[k]
            res += f"  {k}:"
            if isinstance(v, Summarisable):
                if max_depth is None or max_depth > 0:
                    res += textwrap.indent(min_summary(v,subs_max_depth), '  ')
                else:
                    res += f" {repr(v)}"
            else:
                str_v = f" {v}"
                str_v = str_v.replace("\n", " ")
                if max_entry_length is not None and len(str_v) > max_entry_length:
                    str_v = str_v[:max_entry_length - 4] + " ..."
                res += str_v
            if i != len(summary_state) - 1:
                res += "\n"
        return res

def min_plots_grid(logger, output_dir=None, to_grid_parameters={}, fitness_domain=None):
    """Make all default plots for algorithms using grid-based or grid-convertible containers."""
    container = logger.algorithms[0].container # XXX
    if output_dir is None:
        output_dir = logger.log_base_path


    plots.plot_evals(logger, os.path.join(output_dir, "./evals_fitnessmax0.svg"), "max0", ylabel="Fitness")
    plots.plot_iterations(logger, os.path.join(output_dir, "./qd_score.svg"), "qd_score", ylabel="Qd_score_norm")
    ylim_contsize = (0, len(container)) if np.isinf(container.capacity) else (0, container.capacity)
    plots.plot_evals(logger, os.path.join(output_dir, "./evals_contsize.svg"), "cont_size", ylim=ylim_contsize, ylabel="Container size")
    plots.plot_iterations(logger, os.path.join(output_dir, "./iterations_nbupdated.svg"), "nb_updated", ylabel="Number of updated bins")

    if isinstance(container, containers.Grid):
        grid = container
    else:
        if 'shape' not in to_grid_parameters:
            to_grid_parameters['shape'] = (32,) * len(container.features_domain)
        grid = container.to_grid(**to_grid_parameters)

    plot_path = os.path.join(output_dir, "performancesGrid.svg")
    cmap_perf = "inferno" if logger.algorithms[0].optimisation_task == "maximisation" else "inferno_r"
    fitness_domain = grid.fitness_domain if fitness_domain is None else fitness_domain
    plots.plotGridSubplots(grid.quality_array[... ,0], plot_path, plt.get_cmap(cmap_perf), grid.features_domain, fitness_domain[0], nbTicks=None) # type: ignore

    plot_path = os.path.join(output_dir, "activityGrid.svg")
    max_activity = np.max(grid.activity_per_bin)
    plots.plotGridSubplots(grid.activity_per_bin, plot_path, plt.get_cmap("Reds", max_activity), grid.features_domain, [0, max_activity], nbTicks=None) # type: ignore

    # For å sikkerhetskopiere all data til senere plots
    d = pd.DataFrame(logger.evals) # Er dataframe
    d.to_csv(os.path.join(output_dir, "./evals.csv"))

    d = pd.DataFrame(logger.iterations) # Er dataframe 
    d.to_csv(os.path.join(output_dir, "./iterations.csv"))

    d = pd.DataFrame(grid.quality_array[... ,0]) # Er array 
    d.to_csv(os.path.join(output_dir, "./grid.quality_array.csv"))


    d = pd.DataFrame(dict_to_2Darray(grid.quality, shape=grid.shape)) # Dict -> 2d numpy array
    d.to_csv(os.path.join(output_dir, "./grid.quality.csv"))

    d = pd.DataFrame(grid.items) # Liste med løsninger
    d.to_csv(os.path.join(output_dir, "./grid.items.csv"))

    d = pd.DataFrame(grid.nb_items_per_bin) #Er Np array
    d.to_csv(os.path.join(output_dir, "./grid.nb_items_per_bin.csv"))

    d = pd.DataFrame(grid.activity_per_bin) # Er nparray
    d.to_csv(os.path.join(output_dir, "./grid.activity_per_bin.csv"))

    d = pd.DataFrame(dict_to_2Darray(grid.features, shape=grid.shape, feature=True)) # Dict -> 2d numpy array
    d.to_csv(os.path.join(output_dir, "./grid.features.csv"))

    d = pd.DataFrame(grid.recentness) # Liste til hva??
    d.to_csv(os.path.join(output_dir, "./grid.recentness.csv"))

    d = pd.DataFrame(dict_to_2Darray(grid.solutions, shape=grid.shape, individ=True)) # Dict -> 2d numpy array
    d.to_csv(os.path.join(output_dir, "./grid.solutions.csv"))
