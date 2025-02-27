import pickle

import pandas as pd

def csv_to_pkl(file_name : str) -> bool:
    df = pd.read_csv(file_name + ".csv")

    question_df = df.loc[:, 'Question']
    answer_df = df.loc[:, 'Correct Answer']

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


    if (list_to_pkl(file_name, question, 1) and list_to_pkl(file_name, answer, 0)):
        return True

    return False

def list_to_pkl(
        file_name : str,
        target_list : list,
        question_or_answer : bool
        ) -> bool:

    print(f"writing {file_name}")

    if (question_or_answer):
       final_file_name = file_name + "_question.pkl"

    else:
       final_file_name = file_name + "_answer.pkl"

    with open(final_file_name, "wb") as file:
        try:
            pickle.dump(target_list, file)
        except:
            print(f"error on writing {final_file_name}")
            return False

    return True

def main():
    file_name = ["gpqa_diamond"]

    for name in file_name:
        print(csv_to_pkl(name))

if __name__ == "__main__":
    main()
