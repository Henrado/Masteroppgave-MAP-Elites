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


class SineController(Controller):
    def __init__(self, A : float, f : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = A
        self.amplitude_scale = 1.0

        self.frequence = f

        self.phi = phi*np.pi
        self.theta = theta

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.sin(2*np.pi*time*self.frequence + self.phi) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 4
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 2
    
class SineControllerUfq(Controller):
    def __init__(self, A : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = A
        self.amplitude_scale = 1.0

        self.phi = phi*np.pi
        self.theta = theta

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.sin(2*np.pi*time + self.phi) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 3
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 1
    
class TanhController(Controller):
    def __init__(self, A : float, theta : float):
        # Setup initial controller values
        self.amplitude = A
        self.amplitude_scale = 1.0

        self.theta = theta

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.tanh(4*np.sin(2*np.pi*(time + self.theta)))
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 2
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 1

class TanhControllerWOff(Controller):
    def __init__(self, A : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = A
        self.theta = theta
        self.amplitude_scale = 1.0

        self.phi = phi

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.tanh(4*np.sin(2*np.pi*(time + self.phi))) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 3
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 1

class TanhControllerWOffFq(Controller):
    def __init__(self, A : float, f : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = A
        self.theta = theta
        self.f = f
        self.amplitude_scale = 1.0

        self.phi = phi

    def get_action(self, time, observation=None) -> float:
        controller_value = self.amplitude * np.tanh(4*np.sin(2*np.pi*(time*self.f + self.phi))) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale)
    
    @classmethod
    def get_count_variables(cls) -> int:
        return 4
    
    @classmethod
    def get_count_possibleLoc(cls) -> int:
        return 2