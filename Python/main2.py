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
    group_evolution.add_argument('-p', '--population_size', type=int, default=10)
    group_evolution.add_argument('-cr', '--crossover_probability', type=float, default=0.0)
    group_evolution.add_argument('-dim', '--map_dimensions', type=int, default=3)
    group_evolution.add_argument('-res', '--map_resolution', type=int, default=5)
    group_evolution.add_argument('-n', '--evaluation_steps', type=int, default=50)
    args = parser.parse_args()
    ind_domain = (-2., 2.)
    try:
        individ = Individual
        controller = SineController 
        count_leg = 4
        actuators_leg = 3
        params_actuators = 4

        dimension = count_leg*actuators_leg*params_actuators
        dimension_shape = (count_leg, actuators_leg, params_actuators)

        # Lager evaluator:
        env = UnityEvaluator(args.evaluation_steps, editor_mode=True, headless=False, worker_id=0, individ=individ, controller=SineController, genom_shape=dimension_shape)
        # Lager MAP-ELITES:
        grid = containers.Grid(shape=(5,5,5), max_items_per_bin=1, fitness_domain=((-30, 30),), features_domain=((-10, 10), (-10, 10), (-10, 10)))
        algo = algorithms.RandomSearchMutPolyBounded(grid, budget=20, batch_size=15,
                                                     dimension=dimension, optimisation_task="maximisation", ind_domain=ind_domain)
        # Create a logger to pretty-print everything and generate output data files
        logger = algorithms.TQDMAlgorithmLogger(algo)
        
        with ParallelismManager("none") as pMgr:
            best = algo.optimise(env.evaluate, executor = pMgr.executor, batch_mode=False) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch

        print("\n" + algo.summary())

        # Plot the results
        plots.default_plots_grid(logger, output_dir="test_resultat")

        print("\nAll results are available in the '%s' pickle file." % logger.final_filename)
        
    finally:
        env.close()
        

