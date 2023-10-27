from Unity.Unity_evaluator import UnityEvaluator
from EA.MapElites import MapElites
from EA.Individual import Individual
from EA.Sine_controller import SineController
import numpy as np
import argparse
from qdpy import algorithms, containers, plots
from qdpy.base import ParallelismManager
import math


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group_evolution = parser.add_argument_group("Evolution parameters")
    group_evolution.add_argument('-res', '--map_resolution', type=int, default=5)
    group_evolution.add_argument('-n', '--evaluation_steps', type=int, default=100)
    args = parser.parse_args()
    
    
    individ = Individual # Type individ, finnes bare en til nå
    controller = SineController # Type kontroller til individ, finnes bare 

    # Variabel dimensjoner:
    count_leg = 4
    actuators_leg = 3
    params_actuators = 4
    dimension_count = count_leg*actuators_leg*params_actuators
    dimension_shape = (count_leg, actuators_leg, params_actuators)

    # MAP-ELITES variabler: 
    ind_domain = (-1., 1.) # Min og MAX for hver variabel i genomet 
    grid_shape = (args.map_resolution, args.map_resolution, args.map_resolution) # default: (5,5,5)
    fitnes_min = -0
    fitnes_max = 1
    feature_shape_pos = (-5, 5)
    feature_shape_rot = (-20, 20)

    output = "test_resultat"

    # Lager MAP-ELITES:
    # grid = containers.Grid(shape=grid_shape, max_items_per_bin=1, fitness_domain=((fitnes_min, fitnes_max),), features_domain=(feature_shape_rot, feature_shape_pos, feature_shape_pos))
    grid = containers.Grid(shape=(args.map_resolution, args.map_resolution), max_items_per_bin=1, fitness_domain=((fitnes_min, fitnes_max),), features_domain=(feature_shape_pos, feature_shape_pos))
    algo = algorithms.RandomSearchMutPolyBounded(grid, budget=30, batch_size=5,
                                                    dimension=dimension_count, optimisation_task="minimisation", ind_domain=ind_domain)
    # Create a logger to pretty-print everything and generate output data files
    logger = algorithms.TQDMAlgorithmLogger(algo, save_period=2)
    
    try:
        # Lager evaluator:
        env = UnityEvaluator(args.evaluation_steps, editor_mode=True, headless=False, worker_id=0, individ=individ, controller=SineController, genom_shape=dimension_shape)
        
        with ParallelismManager("none") as pMgr:
            best = algo.optimise(env.evaluate, executor = pMgr.executor, batch_mode=False) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch

        print("\n" + algo.summary())

        # Plot the results
        plots.default_plots_grid(logger, output_dir=output)

        print("\nAll results are available in the '%s' pickle file." % logger.final_filename)
    finally:
        env.close()
    
        

