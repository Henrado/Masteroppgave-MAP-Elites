from EA.Individual import Individual
from Unity.RobotParameterChannel import RobotParameterChannel
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

    def shortestAngle(self, from_deg: float, to_deg: float) -> float:
        diff = from_deg - to_deg
        while ((diff >  180).any()): diff[diff >  180] -= 2*180
        while ((diff < -180).any()): diff[diff < -180] += 2*180
        return diff

    def evaluate(self, individ: Individual):
        DELTA_TIME = 0.2
        AMPLITUDE = 2
        N_EVALUATIONS = 20
        MAX_N_STEPS_PER_EVALUATION = 100
        N_GENERATIONS = 20


        self.env.reset()
        individual_name = list(self.env._env_specs)[0] # Henter mlagentene vil her være: Qutee_behavior
        fitness = 0
        end_position = np.zeros((1,3))
        end_rotation = 0
        last_rotation = 0 # Denne kan ikke være np.zeros((1,3)) siden da vil last_rotation bli = [[x,y,z]] ikke [x,y,z]
        for time in range(MAX_N_STEPS_PER_EVALUATION): # max antall steps per episode
            obs,other = self.env.get_steps(individual_name)
            if (len(obs.agent_id)>0):
                # random actions
                # action = np.random.rand(1,12) # Lager tilfeldige vinkler den skal treffe
                action = individ.get_actions(time*DELTA_TIME)
                                            # Lagt opp slik:
                                            # [leg0, upperleg0, forleg0, leg1 ...]
                                            # Der verdien skal være mellom -1 til 1
                                            # Faktisk max verdi kan settes i unity 
                # uncomment below for sine wave actions
                #for i in range(len(action[0])):
                #    action[0,i] = np.sin(j * DELTA_TIME)

                #print(obs.agent_id) # Henter agentenes id
                end_position = obs[0].obs[0][:3] # Henter observasjonene til agent 0 
                end_rotation += self.shortestAngle(obs[0].obs[0][3:6],last_rotation)
                last_rotation = obs[0].obs[0][3:6]
                #print(obs[0].reward) # Henter rewarden til agent 0

                for id in obs.agent_id: # Går gjennom alle agenter og setter dems actions 
                    self.env.set_action_for_agent(individual_name,id,ActionTuple(action))
                self.env.step() #Når all data er satt setter man et setp
                
            else:
                print("Ingen obs fanget opp")
        return fitness, (end_position, end_rotation)