import pickle
    # You may want to import your own packages if the pickle file contains custom objects

with open("iteration-2.p", "rb") as f:
    data = pickle.load(f)
print(data)