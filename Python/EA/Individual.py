from deap import base

class _Fitness(base.Fitness):
    def __init__(self):
        self.weights = 0

class Individual:
    def __init__(self, genom ,pos=None):
        self.rng = None
        self.fitness = _Fitness()
        self.distance_moved = None
        self.genom = genom
        self.map_position = pos

    def getEndPosition(self):
        return self.map_position
    
    def getFitness(self):
        return self.fitness
    

