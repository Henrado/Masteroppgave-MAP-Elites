from EA.Individual import Individual
from Qutee_Interface.interface import Qutee_interface
from Unity.fitness_funtions import basicFitness
from Unity.RobotParameterChannel import RobotParameterChannel
from mlagents_envs.environment import UnityEnvironment
from mlagents_envs.base_env import ActionTuple
import time
import numpy as np
import os
import struct
import platform 


class UnityEvaluator:
    def __init__(self, evaluation_steps, editor_mode=False, headless=False, worker_id=0, individ=None, controller=None, genom_shape=None):
        self.MAX_N_STEPS_PER_EVALUATION = evaluation_steps
        self.BUILD_PATH = self._getBuild_Path()
        if editor_mode:
            self.env = UnityEnvironment(file_name=None, seed=1)
        elif headless:
            self.env = UnityEnvironment(file_name=self.BUILD_PATH, seed=1, no_graphics=True, worker_id=worker_id)
        else:
            self.env = UnityEnvironment(file_name=self.BUILD_PATH, seed=1, no_graphics=False, worker_id=worker_id)

        self.individ = individ
        self.controller = controller
        self.genom_shape = genom_shape

    def _getBuild_Path(self) -> str:
        plt = platform.system()
        if plt == "Windows":
            return "../Build/Windows/Figur2.exe"
        elif plt == "Linux":
            return "../Build/Linux/Figur2.x86_64"
        elif plt == "Darwin":
            raise NotImplementedError("Mac er ikke implementer ennå")
        else:
            print("Unidentified system")
            raise NotImplementedError("OS ikke gjennkjent")

    def close(self):
        self.env.close()

    def shortestAngle(self, from_deg: float, to_deg: float) -> float:
        diff = from_deg - to_deg
        while ((diff >  180).any()): diff[diff >  180] -= 2*180
        while ((diff < -180).any()): diff[diff < -180] += 2*180
        return diff

    def evaluate(self, ind, realRobot=False):
        DELTA_TIME = 0.2
        if realRobot:
            Q = Qutee_interface.Qutee_interface()
            Q.EnableTorqueALL()
        genom = np.array(ind[:]).reshape(self.genom_shape)
        individ = self.individ(genom, self.controller)
        self.env.reset()
        individual_name = list(self.env._env_specs)[0] # Henter mlagentene vil her være: Qutee_behavior
        end_position = np.zeros((1,3))
        end_rotation = 0
        last_rotation = 0 # Denne kan ikke være np.zeros((1,3)) siden da vil last_rotation bli = [[x,y,z]] ikke [x,y,z]
        for t in range(self.MAX_N_STEPS_PER_EVALUATION): # max antall steps per episode
            obs,other = self.env.get_steps(individual_name)
            if (len(obs.agent_id)>0):
                # random actions
                # action = np.random.rand(1,12) # Lager tilfeldige vinkler den skal treffe
                action = individ.get_actions(t*DELTA_TIME)
                                            # Lagt opp slik:
                                            # [leg0, upperleg0, forleg0, leg1 ...]
                                            # Der verdien skal være mellom -1 til 1
                                            # Faktisk max vinkel kan settes i unity 
                #action = np.zeros((1,12))
                #print(obs.agent_id) # Henter agentenes id
                end_position = obs[0].obs[0][:3] # Henter observasjonene til agent 0 
                end_rotation += self.shortestAngle(obs[0].obs[0][3:6],last_rotation)
                last_rotation = obs[0].obs[0][3:6]
                #print(obs[0].reward) # Henter rewarden til agent 0
                if realRobot:
                    Q.setAction(action[0])

                for id in obs.agent_id: # Går gjennom alle agenter og setter dems actions 
                    self.env.set_action_for_agent(individual_name,id,ActionTuple(action))
                self.env.step() #Når all data er satt setter man et setp
            else:
                print("Ingen obs fanget opp")
        end_x = end_position[0]
        end_z = end_position[2]
        end_yrot = end_rotation[1] # type: ignore
        fitness = basicFitness(end_x, end_z, end_yrot)
        # print(fitness, end_yrot, end_x, end_z)
        if realRobot:
            Q.DisableTorqueALL()
            Q.quit()
        return (fitness,), (end_x, end_z)
    