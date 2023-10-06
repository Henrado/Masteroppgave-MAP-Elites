import random
import argparse
import itertools
import numpy as np
import multiprocessing as mp
from deap import base
from deap import tools

class MapElites:
    def __init__(self, args):
        self.steps = 0
        self.crossover_probability = args.crossover_probability
        self.args = args

        # Evaluation setup
        self.evaluation_steps = args.evaluation_steps

        # Population setup
        self.population_size = args.population_size
        #self.population = createNPopulation(n=self.population_size)
        self.population = [i for i in range(self.population_size)]

        # Map setup
        self.map_dimensions = args.map_dimensions
        self.map_sizes = tuple([args.map_resolution for _ in range(self.map_dimensions)])
        #self.map_shape = tuple([self.map_sizes[x] for x in range(self.map_dimensions)])
        #self.map = np.full((self.map_dimensions, args.map_resolution, args.map_resolution), None)
        self.map = np.full(self.map_sizes, None)
        
        print(self.map)
        print(self.map.shape)

    def placeIndivideInMap(self, individ):
        position = individ.getEndPosition()
        roundPosition = np.rint(position)
        self.map[roundPosition] = 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group_evolution = parser.add_argument_group("Evolution parameters")
    group_evolution.add_argument('-p', '--population_size', type=int, default=64)
    group_evolution.add_argument('-cr', '--crossover_probability', type=float, default=0.0)
    group_evolution.add_argument('-dim', '--map_dimensions', type=int, default=2)
    group_evolution.add_argument('-res', '--map_resolution', type=int, default=5)
    group_evolution.add_argument('-n', '--evaluation_steps', type=int, default=5000)
    args = parser.parse_args()
    map = MapElites(args)