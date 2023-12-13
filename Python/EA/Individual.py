import numpy as np
from abc import ABC, abstractmethod 
from Controllers import *

class Individ(ABC): 
  
    @abstractmethod
    def get_actions(self, time:float, observation=None) -> float:
        return
    
    @classmethod
    @abstractmethod
    def get_count_variables(cls) -> int:
        return 4


class Individual_zeroLocked:
    COUNT_LEG = 4
    ACTUATOR_LEG = 3
    PARAMS_ACTUATORS = 4

    def __init__(self, genom, controller):
        self.genom = genom
        self.controllers = self._initControllers(controller, genom)

    def _initControllers(self, controller, genom):
        genom = np.array(genom).reshape(self.get_dimension_shape(controller))
        # genom er lagt opp slik:
        # [[A_con1, f_con1, phi_con1, theta_con1]
        #  [A_con2, f_con2, phi_con2, theta_con2]
        #  ...]
        print(genom)
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
    
    @classmethod
    def get_dimension_count(cls, con:Controller):
        cls.PARAMS_ACTUATORS = con.get_count_variables()
        return cls.COUNT_LEG * cls.ACTUATOR_LEG * cls.PARAMS_ACTUATORS
    
    @classmethod
    def get_dimension_shape(cls, con:Controller):
        cls.PARAMS_ACTUATORS = con.get_count_variables()
        return (cls.COUNT_LEG, cls.ACTUATOR_LEG, cls.PARAMS_ACTUATORS)
    

class Individual_twoLock:
    COUNT_A = 3
    COUNT_F = 3

    COUNT_LEG = 4
    ACTUATOR_LEG = 3
    PARAMS_ACTUATORS = 2
    COUNT_FI_TH = COUNT_LEG * ACTUATOR_LEG * PARAMS_ACTUATORS

    def __init__(self, genom, controller):
        self.genom = genom
        self.controllers = self._initControllers(controller, genom)

    def _initControllers(self, controller, genom_raw):
        # genom_raw er lagt opp slik:
        # [A_body, A_upperlegg, A_loverleg, f_body, f_upperleg, 
        # f_loverleg, phi_con1, theta_con1, phi_con2, theta_con2...]

        # Skal bli slik:
        # [[A_body, f_body, phi_con1, theta_con1]
        #  [A_upperleg, f_upperleg, phi_con2, theta_con2]
        #  ...]
        if issubclass(controller, SineController):
            A = np.array(genom_raw[0:3])
            F = np.array(genom_raw[3:6])
            rest = np.array(genom_raw[6:]).reshape((self.COUNT_LEG*self.ACTUATOR_LEG, controller.get_count_possibleLoc()))

            A_all = np.concatenate([A for _ in range(self.COUNT_LEG)])[:, np.newaxis]
            F_all = np.concatenate([F for _ in range(self.COUNT_LEG)])[:, np.newaxis]
            genom = np.concatenate([A_all, F_all, rest], axis=1).reshape((self.COUNT_LEG, self.ACTUATOR_LEG, self.PARAMS_ACTUATORS))
        elif issubclass(controller, TanhController):
            A = np.array(genom_raw[0:3])
            rest = np.array(genom_raw[3:]).reshape((self.COUNT_LEG*self.ACTUATOR_LEG, controller.get_count_possibleLoc()))

            A_all = np.concatenate([A for _ in range(self.COUNT_LEG)])[:, np.newaxis]
            genom = np.concatenate([A_all, rest], axis=1).reshape((self.COUNT_LEG, self.ACTUATOR_LEG, self.PARAMS_ACTUATORS))
        else:
            genom = np.zeros((self.COUNT_LEG, self.ACTUATOR_LEG, self.PARAMS_ACTUATORS))


        print(genom)
        controllers = []
        for leg in range(len(genom)):
            for actuator in range(len(genom[leg])):
                controllers.append(controller(*genom[leg, actuator].T)) # type: ignore
        return controllers

    def get_actions(self, time : float):
        action_angels = np.zeros((1,len(self.controllers)))
        for i in range(len(self.controllers)):
            action_angels[0,i] = self.controllers[i].get_action(time)
        return action_angels
    
    @classmethod
    def get_dimension_count(cls, con:Controller):
        cls.PARAMS_ACTUATORS = con.get_count_variables()
        return (con.get_count_possibleLoc()+cls.COUNT_LEG*(con.get_count_variables()-con.get_count_possibleLoc()))*cls.ACTUATOR_LEG
        #return cls.COUNT_A+cls.COUNT_F+cls.COUNT_LEG*cls.ACTUATOR_LEG*cls.PARAMS_ACTUATORS
    
    @classmethod
    def get_dimension_shape(cls, con:Controller):
        cls.PARAMS_ACTUATORS = con.get_count_variables()
        return (cls.COUNT_LEG, cls.ACTUATOR_LEG, cls.PARAMS_ACTUATORS)


if __name__ == "__main__":
    s = SineController
    ind = Individual_zeroLocked
    count = ind.get_dimension_count(s)
    genom = np.arange(count)
    print(genom)
    a = ind(genom, s)