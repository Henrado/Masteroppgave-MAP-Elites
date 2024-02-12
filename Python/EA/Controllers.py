import numpy as np
from abc import ABC, abstractmethod 

class Controller(ABC): 
  
    @abstractmethod
    def get_action(self, time:float, observation=None) -> float:
        return 0
    
    @classmethod
    @abstractmethod
    def get_count_variables(cls) -> int:
        return 0
    
    @classmethod
    @abstractmethod
    def get_count_possibleLoc(cls) -> int:
        return 0

GENOM_MIN = 0
GENOM_MAX = 1
A_MIN = 0.0
A_MAX = 1.0
F_MIN = 0.5
F_MAX = 2.0
PHI_SIN_MIN = -np.pi
PHI_SIN_MAX = np.pi
PHI_TANH_MIN = 0
PHI_TANH_MAX = 1
THETA_MIN = -0.7
THETA_MAX = 0.7


class SineController(Controller):
    def __init__(self, A : float, f : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = np.interp(A, [GENOM_MIN,GENOM_MAX], [A_MIN, A_MAX])
        self.amplitude_scale = 1.0

        self.frequence = np.interp(f, [GENOM_MIN,GENOM_MAX], [F_MIN, F_MAX])

        self.phi = np.interp(phi, [GENOM_MIN,GENOM_MAX], [PHI_SIN_MIN, PHI_SIN_MAX])
        self.theta = np.interp(theta, [GENOM_MIN, GENOM_MAX], [THETA_MIN, THETA_MAX])

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.sin(2*np.pi*time*self.frequence + self.phi) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale, dtype=float)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 4
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 2
    
class SineControllerUfq(Controller):
    def __init__(self, A : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = np.interp(A, [GENOM_MIN,GENOM_MAX], [A_MIN, A_MAX])
        self.amplitude_scale = 1.0

        self.phi = np.interp(phi, [GENOM_MIN,GENOM_MAX], [PHI_SIN_MIN, PHI_SIN_MAX])
        self.theta = np.interp(theta, [GENOM_MIN, GENOM_MAX], [THETA_MIN, THETA_MAX])

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.sin(2*np.pi*time + self.phi) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale, dtype=float)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 3
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 1
    
class TanhController(Controller):
    def __init__(self, A : float, phi : float):
        # Setup initial controller values
        self.amplitude = np.interp(A, [GENOM_MIN,GENOM_MAX], [A_MIN, A_MAX])
        self.amplitude_scale = 1.0

        self.phi = np.interp(phi, [GENOM_MIN,GENOM_MAX], [PHI_TANH_MIN, PHI_TANH_MAX])

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.tanh(4*np.sin(2*np.pi*(time + self.phi)))
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale, dtype=float)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 2
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 1

class TanhControllerWOff(Controller):
    def __init__(self, A : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = np.interp(A, [GENOM_MIN,GENOM_MAX], [A_MIN, A_MAX])
        self.theta = np.interp(theta, [GENOM_MIN, GENOM_MAX], [THETA_MIN, THETA_MAX])
        self.amplitude_scale = 1.0

        self.phi = self.phi = np.interp(phi, [GENOM_MIN,GENOM_MAX], [PHI_TANH_MIN, PHI_TANH_MAX])

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.tanh(4*np.sin(2*np.pi*(time + self.phi))) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale, dtype=float)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 3
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 1

class TanhControllerWOffFq(Controller):
    def __init__(self, A : float, f : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = np.interp(A, [GENOM_MIN,GENOM_MAX], [A_MIN, A_MAX])
        self.theta = np.interp(theta, [GENOM_MIN, GENOM_MAX], [THETA_MIN, THETA_MAX])
        self.f = np.interp(f, [GENOM_MIN,GENOM_MAX], [F_MIN, F_MAX])
        self.amplitude_scale = 1.0

        self.phi = self.phi = np.interp(phi, [GENOM_MIN,GENOM_MAX], [PHI_TANH_MIN, PHI_TANH_MAX])

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.tanh(4*np.sin(2*np.pi*(time*self.f + self.phi))) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale, dtype=float)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 4
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 2