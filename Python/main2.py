from mlagents_envs.environment import UnityEnvironment
from unity_evaluator import UnityEvaluator
import numpy as np

try:
    env = UnityEvaluator(100, editor_mode=True, headless=False, worker_id=0)
    params = []
    for i in range(4):
        params.append(np.ones((3,4)))
    env.evaluate(params)
finally:
    env.close()
    

