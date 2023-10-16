import numpy as np

class SineController:
    def __init__(self, A : float, f : float, phi : float, theta : float):
        # Setup initial controller values
        self.amplitude = A
        self.amplitude_scale = 1.0

        self.frequence = f

        self.phi = phi
        self.theta = theta

    def get_action(self, time, observation=None):
        controller_value = self.amplitude * np.sin(2*np.pi*time*self.frequence + self.phi) + self.theta
        return np.clip(controller_value, -self.amplitude_scale, self.amplitude_scale)
