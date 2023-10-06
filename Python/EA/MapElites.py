import random
import argparse
import itertools
import numpy as np
import multiprocessing as mp
from deap import base
from deap import tools
from Individual import Individual

class MapElites:
    def __init__(self, args):
        self.steps = 0
        self.crossover_probability = args.crossover_probability
        self.args = args
        self.max_distance_meter = 10;

        # Evaluation setup
        self.evaluation_steps = args.evaluation_steps

        # Population setup
        self.population_size = args.population_size
        self.population = self.initializePopulation(n=self.population_size)

        # Map setup
        self.map_dimensions = args.map_dimensions
        self.map_resolution = args.map_resolution
        self.map_sizes = tuple([args.map_resolution for _ in range(self.map_dimensions)])
        #self.map_shape = tuple([self.map_sizes[x] for x in range(self.map_dimensions)])
        #self.map = np.full((self.map_dimensions, args.map_resolution, args.map_resolution), None)
        self.map = np.full(self.map_sizes, None)
        
        #print(self.map)
        #print(self.map.shape)

    def placeIndivideInMap(self, individ: Individual):
        position = individ.getEndPosition()
        index = np.interp(position, [-self.max_distance_meter, self.max_distance_meter], [0, self.map_resolution-1])
        index = tuple(np.int32(np.rint(index)))
        print(index)
        self.map[index] = individ.getFitness()

    def initializePopulation(self, n : int):
        genom_length = 12
        pop = []
        for i in range(n):
            genom = np.array([np.random() for _ in range(genom_length)])
            pop.append(Individual(genom))
        return pop

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group_evolution = parser.add_argument_group("Evolution parameters")
    group_evolution.add_argument('-p', '--population_size', type=int, default=64)
    group_evolution.add_argument('-cr', '--crossover_probability', type=float, default=0.0)
    group_evolution.add_argument('-dim', '--map_dimensions', type=int, default=3)
    group_evolution.add_argument('-res', '--map_resolution', type=int, default=5)
    group_evolution.add_argument('-n', '--evaluation_steps', type=int, default=5000)
    args = parser.parse_args()
    ind = Individual(np.array([10,0,-5]))
    map = MapElites(args)
    map.placeIndivideInMap(ind)
    print(map.map)