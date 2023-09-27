from mlagents_envs.environment import UnityEnvironment
from unity_evaluator import UnityEvaluator

try:
    env = UnityEvaluator(50, editor_mode=True, headless=False, worker_id=0)
    env.evaluate([1.0, 2.0])
finally:
    env.close()
    

