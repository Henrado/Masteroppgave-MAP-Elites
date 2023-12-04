from Unity.Unity_evaluator import UnityEvaluator
from EA.MapElites import MapElites
from EA.Individual import Individual_48
from EA.Sine_controller import SineController
import numpy as np
import argparse
from qdpy import algorithms, containers, plots
from qdpy.base import ParallelismManager
import math
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group_evolution = parser.add_argument_group("Evolution parameters")
    group_evolution.add_argument('-res', '--map_resolution', type=int, default=10)
    group_evolution.add_argument('-n', '--evaluation_steps', type=int, default=200)
    group_evolution.add_argument('-e', '--experiment_name', type=str, default="test_resultat")
    args = parser.parse_args()
    
    
    individ = Individual_48 # Type individ, finnes bare en til nå
    controller = SineController # Type kontroller til individ, finnes bare 

    # Variabel dimensjoner:
    dimension_count = individ.get_dimension_count()
    dimension_shape = individ.get_dimension_shape()

    # MAP-ELITES variabler: 
    ind_domain = (-1., 1.) # Min og MAX for hver variabel i genomet 
    grid_shape = (args.map_resolution, args.map_resolution, args.map_resolution) # default: (5,5,5)
    fitnes_min = -0
    fitnes_max = 1
    feature_shape_pos = (-5, 5)
    feature_shape_rot = (-20, 20)


    output = os.path.join("result", args.experiment_name)
    try: 
        os.mkdir(output)
    except OSError as error: 
        print(error) 

    # Lager MAP-ELITES:
    # grid = containers.Grid(shape=grid_shape, max_items_per_bin=1, fitness_domain=((fitnes_min, fitnes_max),), features_domain=(feature_shape_rot, feature_shape_pos, feature_shape_pos))
    grid = containers.Grid(shape=(args.map_resolution, args.map_resolution), max_items_per_bin=1, fitness_domain=((fitnes_min, fitnes_max),), features_domain=(feature_shape_pos, feature_shape_pos))
    algo = algorithms.RandomSearchMutPolyBounded(grid, budget=10000, batch_size=500,
                                                    dimension=dimension_count, optimisation_task="minimisation", ind_domain=ind_domain)
    # Create a logger to pretty-print everything and generate output data files
    logger = algorithms.TQDMAlgorithmLogger(algo, save_period=20, log_base_path=output)
    
    try:
        # Lager evaluator:
        env = UnityEvaluator(args.evaluation_steps, editor_mode=False, headless=True, worker_id=0, individ=individ, controller=SineController, genom_shape=dimension_shape)
        
        with ParallelismManager("none") as pMgr:
            best = algo.optimise(env.evaluate, executor = pMgr.executor, batch_mode=False) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch

        print("\n" + algo.summary())

        # Plot the results
        plots.default_plots_grid(logger, output_dir=output)

        print("\nAll results are available in the '%s' pickle file." % logger.final_filename)
    finally:
        env.close()
    
        

