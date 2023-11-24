import pickle
from qdpy import algorithms, containers, plots

    # You may want to import your own packages if the pickle file contains custom objects

with open("result/22.11.2023/final.p", "rb") as f:
    data = pickle.load(f)
grid = data['container']
for i in range(10):
    for j in range(10):
        print("i:", i, "j:", j, grid.solutions[(i,j)])
print(grid.solutions[(5, 1)])
