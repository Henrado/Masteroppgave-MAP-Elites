from unity_interface import RobotParameterChannel
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.base_env import ActionTuple
import time
import numpy as np
import os
import struct

BUILD_PATH=""

class UnityEvaluator:
    def __init__(self, evaluation_steps, editor_mode=False, headless=False, worker_id=0):
        self.steps = evaluation_steps
        self.channel = RobotParameterChannel()
        if editor_mode:
            self.env = UnityEnvironment(file_name=None, seed=1, side_channels=[self.channel])
        elif headless:
            self.env = UnityEnvironment(file_name=BUILD_PATH, seed=1, side_channels=[self.channel], no_graphics=True, worker_id=worker_id)
        else:
            self.env = UnityEnvironment(file_name=BUILD_PATH, seed=1, side_channels=[self.channel], no_graphics=False, worker_id=worker_id)
        self.times_used = 0

    def close(self):
        self.env.close()

    def evaluate(self, config):
        # Setup
        for g in range(self.steps):
            self.channel.send_config(len(config), config)
            print("Sender data")
            # Next sim step
            # Calculating the boids action for each boid
            self.env.step()
        print("Sendt")
        # Simulation