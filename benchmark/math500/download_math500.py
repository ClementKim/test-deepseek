import pickle
import time

import pandas as pd

def download_dataset() -> tuple[list, list]:
    df = pd.read_json("hf://datasets/HuggingFaceH4/MATH-500/test.jsonl", lines=True)

    question_df = df.loc[:, "problem"]
    answer_df = df.loc[:, "answer"]

    question = []
    for q in question_df:
        if q == "\n":
            continue

        question.append(q)

    answer = []
    for a in answer_df:
        if a == "\n":
            continue

        answer.append(a)

    return question, answer

def file_write(
        file_name : str,
        target_list : list
        ) -> bool:

    print(f"writing {file_name}")
    with open(file_name, "wb") as file:
        try:
            pickle.dump(target_list, file)
        except:
            return False

    return True

def main():
    question, answer = download_dataset()

    file_write("./problem_set.pkl", question)
    file_write("./answer_set.pkl", answer)

if __name__ == "__main__":
    main()
