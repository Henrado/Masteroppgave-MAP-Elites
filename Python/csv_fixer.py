import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from track import *


base_dir_real = "../../Master_Resultater/FysiskTest/Determ/Mocap/G_TWoffFq_B/3_linje1_003.csv"
csv = read_csv(base_dir_real, index_col="Frame", skiprows=6)
csv.loc[:, "X.1"] = -csv.loc[:, "X.1"]
csv.loc[:, "Z.1"] = -csv.loc[:, "Z.1"]

rename = {"X.1":"Z.1", "Z.1": "X.1"}
csv = csv.rename(columns=rename, errors="raise")

csv = csv[["Time (Seconds)", "X", "Y", "Z", "X.1", "Y.1", "Z.1"]]
print(csv)
csv.to_csv("test")