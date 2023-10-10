import random
import argparse
import itertools
import numpy as np
import multiprocessing as mp
from deap import base
from deap import tools
from EA.Individual import Individual
from EA.Sine_controller import SineController

class MapElites:
    def __init__(self, args):
        self.steps = 0
        self.crossover_probability = args.crossover_probability
        self.args = args
        self.max_distance_meter = 10
        self.max_rotation_degree = 360

        # Evaluation setup
        self.evaluation_steps = args.evaluation_steps

        # Population setup
        self.population_size = args.population_size
        self.population = self.initializePopulation(n=self.population_size)

        # Map setup
        self.map_dimensions = args.map_dimensions
        self.map_resolution = args.map_resolution
        self.map_sizes = tuple([args.map_resolution for _ in range(self.map_dimensions)])
        self.map = np.full(self.map_sizes, None)
        

    def placeIndivideInMap(self, individ: Individual, fitness, features):
        index_x_z = np.interp(features[:2], [-self.max_distance_meter, self.max_distance_meter], [0, self.map_resolution-1])
        index_yRot = np.interp(features[2], [-self.max_rotation_degree, self.max_rotation_degree], [0, self.map_resolution-1])
        print("features", features)
        index = tuple(np.int32(np.rint(np.concatenate((index_x_z, index_yRot), axis=None))))
        print("index", index)
        if self.map[index] is not None: 
            a = self.map[index].getFitness() 
        else: 
            a = None
        print(fitness, a)
        if self.map[index] is None or fitness > self.map[index].getFitness():
            self.map[index] = individ
        else:
            print("Passer ikke og blir kastet:", features)

    def initializePopulation(self, n : int):
        count_leg = 4
        actuators_leg = 3
        params_actuators = 4
        pop = []
        for i in range(n):
            genom = np.zeros((count_leg,actuators_leg,params_actuators))
            for leg_j in range(count_leg):
                genom[leg_j] = np.random.rand(actuators_leg, params_actuators)
            pop.append(Individual(genom, SineController))
        return pop
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group_evolution = parser.add_argument_group("Evolution parameters")
    group_evolution.add_argument('-p', '--population_size', type=int, default=1)
    group_evolution.add_argument('-cr', '--crossover_probability', type=float, default=0.0)
    group_evolution.add_argument('-dim', '--map_dimensions', type=int, default=3)
    group_evolution.add_argument('-res', '--map_resolution', type=int, default=5)
    group_evolution.add_argument('-n', '--evaluation_steps', type=int, default=5000)
    args = parser.parse_args()
    map = MapElites(args)