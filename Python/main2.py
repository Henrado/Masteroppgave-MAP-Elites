from Unity.Unity_evaluator import UnityEvaluator
from EA.MapElites import MapElites
import numpy as np
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group_evolution = parser.add_argument_group("Evolution parameters")
    group_evolution.add_argument('-p', '--population_size', type=int, default=3)
    group_evolution.add_argument('-cr', '--crossover_probability', type=float, default=0.0)
    group_evolution.add_argument('-dim', '--map_dimensions', type=int, default=3)
    group_evolution.add_argument('-res', '--map_resolution', type=int, default=5)
    group_evolution.add_argument('-n', '--evaluation_steps', type=int, default=5000)
    args = parser.parse_args()
    try:
        env = UnityEvaluator(100, editor_mode=True, headless=False, worker_id=0)
        map = MapElites(args)
        pop = map.population
        for p in pop:
            fitness, features = env.evaluate(p)
            p.map_position = features
            map.placeIndivideInMap(p)

        print("Map:")
        print(map.map)
    finally:
        env.close()
        

