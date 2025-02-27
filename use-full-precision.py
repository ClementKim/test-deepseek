import pickle

import pandas as pd

from sys import argv
from transformers import pipeline

def file_to_list(file_name : str) -> list:
    if (file_name[-4:] == ".csv"):
        df = pd.read_csv(file_name)

        question = df.loc[:, "Question"]

        listed_file = []
        for q in question:
            if q == "\n":
                continue

            listed_file.append(q)

    elif (file_name[-4:] == ".txt"):
        f = open(file_name, "r")

        lines = f.read()

        listed_file = list(lines.split("\n"))
        listed_file.pop()

    elif (file_name[-4:] == ".pkl"):
        with open(file_name, "rb") as f:
            listed_file = pickle.load(f)

    else:
        print("file type error")
        exit(1)

    return listed_file

def run_model(
        questions : list,
        model_number_ipt : str
        ) -> list:

    full_answer = []

    pipe = pipeline("text-generation",
            model = "deepseek-ai/DeepSeek-R1-Distill-Llama-" + model_number_ipt + "B",
            device_map = "auto"
            )

    print(f"operating DeepSeek R1 Distill Llama {model_number_ipt}B")
    for question_number, question in enumerate(questions, start = 1):
        print(f"solving question number {question_number}")
        if not(question):
            break

        full_answer.append(list(pipe(question,
                        max_length = 131072,
                        do_sample = True,
                        truncation = True)))

        print(f"done for question #{question_number}")

    print("done for generating")

    return full_answer

def split_think_and_answer_and_write_file(
        test_name : str,
        generated_list : list
        ) -> bool:
    generated_answer = []

    print("split think and answer and write file function is working")

    for lst in generated_list:
        temp = []
        temporal_string = ""
        for question_number, sentence in enumerate(lst[1], start = 1):
            for index in range(len(sentence)-6, 6, -1):
                if ((index >= 6) and (sentence[index-6:index] == "Answer")):
                    temporal_string = sentence[index:]
                    break

            if (not (temporal_string)):
                temporal_string = sentence

            temp.append([question_number, temporal_string])

        if (not (temp)):
            print("not temp")
            return False

        generated_answer.append([lst[0], temp])

    if (not (generated_answer)):
        print("not generated answer")
        return False

    with open("result/" + test_name[:-4] + ".txt", "w") as file:
        for question_and_answer in generated_answer:
            file.write(question_and_answer[0] + "\n--------------------\n")

            for answer in question_and_answer[1]:
                file.write("question number " + str(answer[0]) + " :\n")
                file.write(str(answer[1]))
                file.write("\n\n")

    print("done for creating txt file")
    return True

def main():
    file_list = [
        # [file name, result is number or string, question is related with politics, answer file (if the result is number)]
        # ["questions/question_logic_original.txt", "string", False, None]
        # ["questions/question_logic.txt", "number", False, "questions/question_logic-answer.txt"],
         ["questions/sample_question.txt", "number", False, "questions/sample_answer.txt"],
         ["questions/sample_question2.txt", "number", False, "questions/sample_answer.txt"]
#        ["benchmark/aime/2024/AIME2024.txt", "string", False, None],
#        ["benchmark/aime/2025/AINE2025.txt", "string", False, None],
#        ["benchmark/math500/problem_set.pkl", "string", False, None],
#        ["benchmark/gpqa/gpqa_diamond_question.pkl", "string", False, None]
    ]

    model_number = argv[1]

    generated_answer = []
    for target_dir in file_list:
        file_name = target_dir[0]

        questions = file_to_list(file_name)

        testing_list = run_model(questions, model_number)

        temp = []
        for i in range(len(testing_list)):
            temp.append(testing_list[i])

        generated_answer.append([target_dir[0], temp])

    if (split_think_and_answer_and_write_file(file_name, generated_answer)):
        print("done")

    else:
        print("error on split think and answer and write file")
        print("returning list file with pickle")

        with open("./result/generated_answer_", "wb") as file:
            try:
                pickle.dump(generated_answer, file)
            except:
                print("failed to return list file with pickle")

if __name__ == "__main__":
    main()
