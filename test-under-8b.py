import pandas as pd

from sys import argv
from transformers import pipeline

def run_model(
        questions : list,
        model_number_ipt : str
        ) -> list:

    full_answer = []

    pipe = pipeline("text-generation",
            model = "deepseek-ai/DeepSeek-R1-Distill-Llama-" + model_number_ipt + "B",
            device_map = "auto"
            )

    for question_number, question in enumerate(questions, start = 1):
        if not(question):
            break

        full_answer.append(list(pipe(question,
                        max_length = 131072,
                        do_sample = True,
                        truncation = True)))

    return full_answer

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

    else:
        print("file type error")
        exit(1)

    return listed_file

def split_think_and_answer_and_write_file(generated_list : list) -> bool:
    generated_answer = []

    for lst in generated_list:
        temp = []
        temporal_string = ""
        for question_number, sentence in enumerate(lst[1], start = 1):
            for index in range(len(sentence)-6, 6, -1):
                if ((index >= 6) and (sentence[index-6:index] == "Answer")):
                    while (sentence[index] == ":" or sentence[index] == "*"):
                        index += 1

                    temporal_string = sentence[index:]
                    break

            if (not (temporal_string)):
                return False

            temp.append([question_number, temporal_string])

        if (not (temp)):
            print("not temp")
            return False

        generated_answer.append([lst[0], temp])

    if (not (generated_answer)):
        print("not generated answer")
        return False

    with open("answer_only-test.txt", "w") as file:
        for question_and_answer in generated_answer:
            file.write(question_and_answer[0] + "\n--------------------")

            for answer in question_and_answer[1]:
                file.write("question number " + str(answer[0]) + " :\n")
                file.write(answer[1])
                file.write("\n\n")

    return True

def main():
    file_list = [
        # [file name, result is number or string, question is related with politics, answer file (if the result is number)]
        # ["questions/question_logic.txt", "number", False, "questions/question_logic-answer.txt"],
        # ["questions/sample_question.txt", "number", False, "questions/sample_answer.txt"]
        ["questions/question_logic_original.txt", "string", False, None]
    ]

#    file_name = 
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

    if (split_think_and_answer_and_write_file(generated_answer)):
        print("done")

    else:
        print("error on split think and answer and write file")

if __name__ == "__main__":
    main()
