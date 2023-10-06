from deap import base
import numpy as np


class _Fitness(base.Fitness):
    def __init__(self):
        self.weights = 0

class Individual:
    def __init__(self, genom ,pos=None):
        self.fitness = _Fitness()
        self.genom = genom
        self.map_position = pos

    def getEndPosition(self):
        return self.map_position
    
    def getFitness(self):
        return self.fitness
    
    def get_actions(self, time):
        return np.random.rand(1,12)
    

