from Unity.Unity_evaluator import UnityEvaluator
from Unity.fitness_funtions import basicFitness, circleFitness
from EA.Individual import Individual_zeroLocked, Individual_twoLock
from EA.Controllers import SineController, TanhController, TanhControllerWOff
from Plot.plots import min_plots_grid, min_summary
import numpy as np
import argparse
from qdpy import algorithms, containers, plots
from qdpy.base import ParallelismManager
import math
import os
import sys
import yaml
import random
from qdpy.base import Factory
import pprint




if __name__ == "__main__":
    # Parser argumenter og conf
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=None, help="Numpy random seed")
    parser.add_argument('-p', '--parallelismType', type=str, default='none', help = "Type of parallelism to use (none, concurrent, scoop)")
    parser.add_argument('-n', '--evaluation_steps', type=int, default=None)
    parser.add_argument('-e', '--editor_mode', type=bool, default=None)
    parser.add_argument('-hl', '--headless', type=bool, default=None)
    parser.add_argument('-c', '--configFile', type=str, default='conf.yaml', help = "Path of the configuration file")
    parser.add_argument('-o', '--outputDir', type=str, default=None, help = "Path of the output log files")
    args = parser.parse_args()
    
    # Retrieve configuration from configFile
    config = yaml.safe_load(open(args.configFile))
    print("Retrieved configuration:")
    print(config)
    print("\n------------------------\n")




    # Find where to put logs
    log_base_path = config.get("log_base_path", ".") if args.outputDir is None else args.outputDir
    output = os.path.join("result", log_base_path)
    try: 
        os.mkdir(output)
    except OSError as error: 
        print(error) 



    # Find random seed
    if args.seed is not None:
        seed = args.seed
    elif "seed" in config:
        seed = config["seed"]
    else:
        seed = np.random.randint(1000000)
        config['seed'] = seed
    # Update and print seed
    np.random.seed(seed)
    random.seed(seed)
    print("Seed: %i" % seed)



    # Loads type of individ, controller and fitnessfunction from config
    assert "individ" in config["Unity"], f"Please specify configuration entry 'individ'."
    conf_individ = config["Unity"]["individ"]
    if conf_individ == "Individual_twoLock":
        individ = Individual_twoLock
    elif conf_individ == "Individual_zeroLocked":
        individ = Individual_zeroLocked
    else:
        individ = None
        raise NotImplementedError
    
    assert "controller" in config["Unity"], f"Please specify configuration entry 'controller'."
    conf_controller = config["Unity"]["controller"]
    if conf_controller == "SineController":
        controller = SineController
    elif conf_controller == "TanhController":
        controller = TanhController
    elif conf_controller == "TanhControllerWOff":
        controller = TanhControllerWOff
    else:
        controller = None
        raise NotImplementedError
    config['algorithms']['dimension'] = individ.get_dimension_count(controller) # type: ignore #Plasserer alt i conf for at qdpy skal ta alt sammen 

    assert "fitnessfunction" in config["Unity"], f"Please specify configuration entry 'fitnessfunction'."
    conf_individ = config["Unity"]["fitnessfunction"]
    if conf_individ == "basicFitness":
        fitnessfunction = basicFitness
    elif conf_individ == "circleFitness":
        fitnessfunction = circleFitness
    else:
        fitnessfunction = None
        raise NotImplementedError



    # Create containers and algorithms from configuration 
    factory = Factory()
    assert "containers" in config, f"Please specify configuration entry 'containers' containing the description of all containers."
    factory.build(config["containers"])
    assert "algorithms" in config, f"Please specify configuration entry 'algorithms' containing the description of all algorithms."
    factory.build(config["algorithms"])
    assert "main_algorithm_name" in config, f"Please specify configuration entry 'main_algorithm' containing the name of the main algorithm."
    algo = factory[config["main_algorithm_name"]]
    container = algo.container



    # Lager loggeren basert på config 
    logger = algorithms.TQDMAlgorithmLogger(algo, save_period=config["logger"]["save_period"], log_base_path=output, config=config)



    # Lager Unity variabler fra config eller terminalen 
    if args.evaluation_steps is None:
        evaluation_steps = config["Unity"]["evaluation_steps"] 
    else:
        evaluation_steps = args.evaluation_steps
        config["Unity"]["evaluation_steps"] = evaluation_steps
    
    if args.editor_mode is None:
        editor_mode = config["Unity"]["editor_mode"] 
    else:
        editor_mode = args.editor_mode
        config["Unity"]["editor_mode"] = editor_mode
    
    if args.headless is None:
        headless = config["Unity"]["headless"] 
    else:
        headless = args.headless
        config["Unity"]["headless"] = headless

    if args.parallelismType is None:
        parallelismType = config["ParallelismManager"]["parallelismType"] 
    else:
        parallelismType = args.parallelismType
        config["ParallelismManager"]["parallelismType"]= parallelismType

    with open(os.path.join(output, args.configFile), 'w') as file:
        yaml.dump(config, file)

    try:
        # Create the channel
        if "Qutee" in config["Qutee"]:
            qutee_config = config["Qutee"]
        else:
            qutee_config = None
        # Lager evaluator:
        # Starter Unity 
        env = UnityEvaluator(evaluation_steps, qutee_config=qutee_config, editor_mode=editor_mode, headless=headless, worker_id=0, individ=individ, controller=controller, fitnessfunction=fitnessfunction)

        # Kjører opptimaliseering 
        with ParallelismManager(parallelismType) as pMgr:
            best = algo.optimise(env.evaluate, executor = pMgr.executor, batch_mode=config["ParallelismManager"]["batch_mode"]) # Disable batch_mode (steady-state mode) to ask/tell new individuals without waiting the completion of each batch



        # Viser info 
        print("\n" + algo.summary())

        with open(os.path.join(output, "./algo.summary.txt"), 'w') as f:
            f.write(min_summary(algo))
        # Plot the results
        min_plots_grid(logger, output_dir=output)

        print("\nAll results are available in the '%s' pickle file." % logger.final_filename)
    finally:
        env.close() 
    
        

