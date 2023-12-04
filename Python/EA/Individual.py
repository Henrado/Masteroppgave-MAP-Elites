import numpy as np

class Individual_48:
    COUNT_LEG = 4
    ACTUATOR_LEG = 3
    PARAMS_ACTUATORS = 4

    def __init__(self, genom, controller):
        self.genom = genom
        self.controllers = self._initControllers(controller, genom)

    def _initControllers(self, controller, genom):
        genom = np.array(genom).reshape(self.get_dimension_shape())
        # genom er lagt opp slik:
        # [[A_con1, f_con1, phi_con1, theta_con1]
        #  [A_con2, f_con2, phi_con2, theta_con2]
        #  ...]
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
    def get_dimension_count(cls):
        return cls.COUNT_LEG * cls.ACTUATOR_LEG * cls.PARAMS_ACTUATORS
    
    @classmethod
    def get_dimension_shape(cls):
        return (cls.COUNT_LEG, cls.ACTUATOR_LEG, cls.PARAMS_ACTUATORS)
    

class Individual_30:
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

        A = np.array(genom_raw[0:3])
        F = np.array(genom_raw[3:6])
        rest = np.array(genom_raw[6:]).reshape((self.COUNT_LEG*self.ACTUATOR_LEG, self.PARAMS_ACTUATORS))

        A_all = np.concatenate([A for _ in range(self.COUNT_LEG)])[:, np.newaxis]
        F_all = np.concatenate([F for _ in range(self.COUNT_LEG)])[:, np.newaxis]
        genom = np.concatenate([A_all, F_all, rest], axis=1).reshape((self.COUNT_LEG, self.ACTUATOR_LEG, self.PARAMS_ACTUATORS+2))

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
    def get_dimension_count(cls):
        return cls.COUNT_A+cls.COUNT_F+cls.COUNT_FI_TH
    
    @classmethod
    def get_dimension_shape(cls):
        return (cls.COUNT_LEG, cls.ACTUATOR_LEG, cls.PARAMS_ACTUATORS)
