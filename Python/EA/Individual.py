from deap import base

class _Fitness(base.Fitness):
    def __init__(self):
        self.weights = (1.0, 1.0)

class Individual:
    def __init__(self):
        self.rng = None
        self.fitness = _Fitness()
        self.distance_moved = None
        self.map_position = None

    def getEndPosition(self):
        return self.map_position
