from Unity.Unity_evaluator import UnityEvaluator
from EA.MapElites import MapElites
from EA.Individual import Individual
from EA.Sine_controller import SineController
import numpy as np
import argparse
from qdpy import algorithms, containers, plots
from qdpy.base import ParallelismManager
import math
import os



ind = np.array([0.48756968292376146, 0.39640734381815923, -0.03207644652212038, 0.24265365709548137, 0.8550142124786901, 0.5464029375062585, 0.17257735601180801, 0.4243453187142534, -0.9495004848036142, 0.39475831878655354, 0.5339192080206105, -0.9803351856771438, 0.8910855701720741, -0.6673270491389225, 0.3940192187672651, -0.8236021385572971, 0.7618005228562197, -0.8589349564999043, 0.7008658470007034, -0.28640736809135814, 0.05705316890244716, 0.5346425072768815, -0.9098338578161032, 0.45201868103425147, 0.48132346152856265, 0.9680821212030855, -0.12747508143218855, 0.2558562617257518, -0.4774864290968419, -0.06031849360473296, 0.6841350207925647, 0.19174609859282388, 0.8653654622102673, 0.6294845314523694, -0.5087691818872964, 0.6171186014841978, -0.27712177196433907, -0.6852940349304639, -0.12223714312944312, 0.4579504682180895, 0.9806151740035143, -0.0689757719817834, 0.35677571816046094, 0.8659790041606694, -0.3847738298365213, -0.5923653707936187, -0.041694685856909386, 0.6378015553635297])

individ = Individual # Type individ, finnes bare en til nå
controller = SineController # Type kontroller til individ, finnes bare 

count_leg = 4
actuators_leg = 3
params_actuators = 4
dimension_count = count_leg*actuators_leg*params_actuators
dimension_shape = (count_leg, actuators_leg, params_actuators)

try:
    # Lager evaluator:
    env = UnityEvaluator(500, editor_mode=False, headless=False, worker_id=0, individ=individ, controller=SineController, genom_shape=dimension_shape)
        
    env.evaluate(ind)

finally:
    env.close()
    