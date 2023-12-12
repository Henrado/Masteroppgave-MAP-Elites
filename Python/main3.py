from Unity.Unity_evaluator import UnityEvaluator
from Unity.fitness_funtions import basicFitness, circleFitness
from EA.Individual import Individual_48, Individual_30
from EA.Sine_controller import SineController
import numpy as np
import argparse
from qdpy import algorithms, containers, plots
from qdpy.base import ParallelismManager
import math
import os
import yaml
import random
from qdpy.base import Factory
import pprint


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None, help="Numpy random seed")
    parser.add_argument('-p', '--parallelismType', type=str, default='none', help = "Type of parallelism to use (none, concurrent, scoop)")
    parser.add_argument('-n', '--evaluation_steps', type=int, default=200)
    parser.add_argument('-c', '--configFile', type=str, default='examples/conf/rastrigin.yaml', help = "Path of the configuration file")
    parser.add_argument('-o', '--outputDir', type=str, default=None, help = "Path of the output log files")
    args = parser.parse_args()
    
    # Retrieve configuration from configFile
    config = yaml.safe_load(open(args.configFile))
    print("Retrieved configuration:")
    print(config)
    print("\n------------------------\n")

    # Find where to put logs
    log_base_path = config.get("log_base_path", ".") if args.outputDir is None else args.outputDir

    # Find random seed
    if args.seed is not None:
        seed = args.seed
    elif "seed" in config:
        seed = config["seed"]
    else:
        seed = np.random.randint(1000000)

    # Update and print seed
    np.random.seed(seed)
    random.seed(seed)
    print("Seed: %i" % seed)

    config['algorithms']['dimension'] = 10000

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(config)
    

    

    
    individ = Individual_30 # Type individ, finnes bare en til nå
    controller = SineController # Type kontroller til individ, finnes bare 
    fitnessfunction = basicFitness

    # Variabel dimensjoner:
    dimension_count = individ.get_dimension_count()


    output = os.path.join("result", args.experiment_name)
    try: 
        os.mkdir(output)
    except OSError as error: 
        print(error) 

    # Lager MAP-ELITES:
    # grid = containers.Grid(shape=grid_shape, max_items_per_bin=1, fitness_domain=((fitnes_min, fitnes_max),), features_domain=(feature_shape_rot, feature_shape_pos, feature_shape_pos))
    #grid = containers.Grid(shape=(args.map_resolution, args.map_resolution), max_items_per_bin=1, fitness_domain=((fitnes_min, fitnes_max),), features_domain=(feature_shape_pos, feature_shape_pos))
    #algo = algorithms.RandomSearchMutPolyBounded(grid, budget=10000, batch_size=500,
     #                                               dimension=dimension_count, optimisation_task="maximisation", ind_domain=ind_domain)
    # Create a logger to pretty-print everything and generate output data files
    
    # Create containers and algorithms from configuration 
    factory = Factory()
    assert "containers" in config, f"Please specify configuration entry 'containers' containing the description of all containers."
    factory.build(config["containers"])
    assert "algorithms" in config, f"Please specify configuration entry 'algorithms' containing the description of all algorithms."
    factory.build(config["algorithms"])
    assert "main_algorithm_name" in config, f"Please specify configuration entry 'main_algorithm' containing the name of the main algorithm."
    algo = factory[config["main_algorithm_name"]]
    container = algo.container
    
    logger = algorithms.TQDMAlgorithmLogger(algo, save_period=20, log_base_path=output, config=config)

    try:
        # Lager evaluator:
        env = UnityEvaluator(args.evaluation_steps, editor_mode=False, headless=False, worker_id=0, individ=individ, controller=controller, fitnessfunction=fitnessfunction)
        
        with ParallelismManager("none") as pMgr:
            best = algo.optimise(env.evaluate, executor = pMgr.executor, batch_mode=False) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch

        print("\n" + algo.summary())

        # Plot the results
        plots.default_plots_grid(logger, output_dir=output)

        print("\nAll results are available in the '%s' pickle file." % logger.final_filename)
    finally:
        env.close() 
    
        

