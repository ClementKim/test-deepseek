import pickle

with open("result.pickle", "rb") as fr:
    data = pickle.load(fr)

for key, value in data.items():
    print(key, value)
