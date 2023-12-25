from qdpy import algorithms, containers, plots
import os
import numpy as np
import matplotlib.pyplot as plt
from qdpy import containers
from qdpy import algorithms
import json
import pandas as pd

def min_plots_grid(logger, output_dir=None, to_grid_parameters={}, fitness_domain=None):
    """Make all default plots for algorithms using grid-based or grid-convertible containers."""
    container = logger.algorithms[0].container # XXX
    if output_dir is None:
        output_dir = logger.log_base_path


    plots.plot_evals(logger, os.path.join(output_dir, "./evals_fitnessmax0.pdf"), "max0", ylabel="Fitness")
    plots.plot_iterations(logger, os.path.join(output_dir, "./qd_score.pdf"), "qd_score", ylabel="Qd_score_norm")
    ylim_contsize = (0, len(container)) if np.isinf(container.capacity) else (0, container.capacity)
    plots.plot_evals(logger, os.path.join(output_dir, "./evals_contsize.pdf"), "cont_size", ylim=ylim_contsize, ylabel="Container size")
    plots.plot_iterations(logger, os.path.join(output_dir, "./iterations_nbupdated.pdf"), "nb_updated", ylabel="Number of updated bins")

    if isinstance(container, containers.Grid):
        grid = container
    else:
        if 'shape' not in to_grid_parameters:
            to_grid_parameters['shape'] = (32,) * len(container.features_domain)
        grid = container.to_grid(**to_grid_parameters)

    plot_path = os.path.join(output_dir, "performancesGrid.pdf")
    cmap_perf = "inferno" if logger.algorithms[0].optimisation_task == "maximisation" else "inferno_r"
    fitness_domain = grid.fitness_domain if fitness_domain is None else fitness_domain
    plots.plotGridSubplots(grid.quality_array[... ,0], plot_path, plt.get_cmap(cmap_perf), grid.features_domain, fitness_domain[0], nbTicks=None) # type: ignore

    plot_path = os.path.join(output_dir, "activityGrid.pdf")
    max_activity = np.max(grid.activity_per_bin)
    plots.plotGridSubplots(grid.activity_per_bin, plot_path, plt.get_cmap("Reds", max_activity), grid.features_domain, [0, max_activity], nbTicks=None) # type: ignore

    # For å sikkerhetskopiere all data til senere plots
    d = pd.DataFrame(logger.evals)
    with open(os.path.join(output_dir, "./evals.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(logger.iterations)
    with open(os.path.join(output_dir, "./iterations.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(grid.quality_array[... ,0])
    with open(os.path.join(output_dir, "./grid.quality_array.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(grid.quality)
    with open(os.path.join(output_dir, "./grid.quality.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(grid.items)
    with open(os.path.join(output_dir, "./grid.items.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(grid.nb_items_per_bin)
    with open(os.path.join(output_dir, "./grid.nb_items_per_bin.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(grid.activity_per_bin)
    with open(os.path.join(output_dir, "./grid.activity_per_bin.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(grid.features)
    with open(os.path.join(output_dir, "./grid.features.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(grid.recentness)
    with open(os.path.join(output_dir, "./grid.recentness.json"), 'w') as f:
        json.dump(d.to_dict(), f)

    d = pd.DataFrame(grid.solutions)
    with open(os.path.join(output_dir, "./grid.solutions.json"), 'w') as f:
        json.dump(d.to_dict(), f)
