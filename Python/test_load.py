import pickle
    # You may want to import your own packages if the pickle file contains custom objects

with open("result/10.11.23/final.p", "rb") as f:
    data = pickle.load(f)
grid = data['container']
print(grid.solutions[(4, 9)])
