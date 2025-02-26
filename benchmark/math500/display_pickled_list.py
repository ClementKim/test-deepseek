import pickle
import time

with open("problem_set.pkl", "rb") as f:
    load_list = pickle.load(f)

print(load_list[13])
exit(1)

for i in load_list:
    print(i)
    print("\n")
