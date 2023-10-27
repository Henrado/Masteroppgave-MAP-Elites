import numpy as np

class Individual:
    def __init__(self, genom, controller):
        self.genom = genom
        self.controllers = self._initControllers(controller, genom)

    def _initControllers(self, controller, genom):
        controllers = []
        for leg in range(len(genom)):
            for actuator in range(len(genom[leg])):
                controllers.append(controller(*genom[leg, actuator].T))
        return controllers

    def get_actions(self, time : float):
        action_angels = np.zeros((1,len(self.controllers)))
        for i in range(len(self.controllers)):
            action_angels[0,i] = self.controllers[i].get_action(time)
        return action_angels
    

