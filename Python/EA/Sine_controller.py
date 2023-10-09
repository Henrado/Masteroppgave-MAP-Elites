import math
import numpy as np

class SineController:
    def __init__(self, A : float, f : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = A
        self.amplitude_scale = 1.0

        self.frequence = f

        self.phi = phi
        self.theta = theta

    def mutate(self, sigma, probability):
        pass

    def gaussian_mutation(self, parameter, sigma):
        new_parameter = parameter
        new_parameter += self.rng.normal(0, sigma)
        while new_parameter >= 1.0 or new_parameter < 0.0:
            if new_parameter >= 1.0:
                new_parameter = 2.0 - new_parameter
            elif new_parameter < 0.0:
                new_parameter = -new_parameter
        return new_parameter

    def get_action(self, time, observation=None):
        controller_value = self.amplitude * np.sin(2*np.pi*time*self.frequence + self.phi) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale)
