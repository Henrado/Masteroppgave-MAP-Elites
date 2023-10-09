from deap import base
import numpy as np

class Individual:
    def __init__(self, genom, controller ,pos=None):
        self.fitness = 0
        self.genom = genom
        self.map_position = pos
        self.controllers = self._initControllers(controller, genom)

    def _initControllers(self, controller, genom):
        controllers = []
        for leg in range(len(genom)):
            for actuator in range(len(genom[leg])):
                controllers.append(controller(*genom[leg, actuator].T))
        return controllers

    def getEndPosition(self):
        return self.map_position
    
    def getFitness(self):
        return self.fitness
    
    def get_actions(self, time):
        action_angels = np.zeros((1,len(self.controllers)))
        # return self.controller.get_action(time)
        for i in range(len(self.controllers)):
            action_angels[0,i] = self.controllers[i].get_action(time)
        return action_angels
    

