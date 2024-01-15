import pandas as pd
import json
import numpy as np



path = "test/evals.csv"
path = "test/iterations.csv"
path = "test/grid.quality.csv"
#path = "test/grid.quality_array.csv"
path = "test/grid.items.csv"
path = "test/grid.nb_items_per_bin.csv"
path = "test/grid.activity_per_bin.csv"
path = "test/grid.features.csv"
path = "test/grid.recentness.csv"
path = "test/grid.solutions.csv"

fil = pd.read_csv(path, index_col=0)
#fil = np.load(path, allow_pickle=True)
arr = fil.to_numpy(dtype=object)
print(arr[63][:])