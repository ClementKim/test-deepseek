import pandas as pd

df = pd.read_csv("gpqa_diamond.csv")

question = df.loc[:, 'Question']
answer = df.loc[:, 'Correct Answer']

with open("GPQA_Diamond_question.txt", "w") as file1:
    for q in question:
        file1.write(q + "\n")

file1.close()

with open("GPQA_Diamond_answer.txt", "w") as file2:
    for a in answer:
        file2.write(a + "\n")

file2.close()
