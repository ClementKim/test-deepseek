import pandas as pd

from sys import argv
from transformers import pipeline

def run_model(
        questions : list,
        model_number_ipt : str
        ) -> list:

    for question_number, question in enumerate(questions, start = 1):
        messages = [{
                "role": "user",
                "content": content
        }]

        if not (content == messages[0]["content"]):
            print("Error in messages content: question number {question_number}")
            exit(1)

        pipe = pipeline("text-generation", model = "deepseek-ai/DeepSeek-R1-Distill-Llama-" + model_number + "B")

        respond = list(pipe(messages))

        # for testing returned msg
        if question_number == 1:
            print(respond)
            exit(1)

def matching_answer(
        answer_list : list,
        model_result_list : list
        ) -> int:

    number_of_matching = 0
    actual_returned_answer = []

    for sentence in model_result_list:
        for index in range(len(sentence)-1, 7, -1):
            if sentence[index-7:index] == "\\boxed{":
                answer = 0
                while sentence[index + anchor] != "}":
                    answer += 1

                actual_returned_answer.append(sentence[index:index + anchor])

    if not (len(actual_returned_answer) == len(answer_lsit)):
        print("Error: the length of actual returned answer list are not matching")

        return -1

    for index in range(len(answer_list)):
        if (int(answer_list[index]) == int(actual_returned_answer[index])):
            number_of_matching += 1

    return number_of_matching

def file_to_list(file_name : str) -> list:
    if (file_name[-4:] == ".csv"):
        df = pd.read_csv(file_name)

        question = df.loc[:, "Question"]

        listed_file = []
        for q in question:
            if q == "\n":
                continue

            listed_file.append(q)

    elif (file_dir[-4:] == ".txt"):
        f = open(file_name, "r")

        lines = f.read()

        listed_file = list(lines.split("\n"))
        question.pop()

    else:
        print("file type error")
        exit(1)

    return listed_file

def main():
    file_list = [
        # [file name, result is number or string, question is related with politics, answer file (if the result is number)]
        ["questions/question_logic.txt", "number", False, "qustions/question_logic-answer.txt"]
    ]

#    file_name = 
    model_number = argv[1]

    for target_dir in file_list:
        questions = file_to_list(file_name)

        for index, question in enumerate(questions, start = 1):
            run_model(question, model_number)

if __name__ == "__main__":
    main()
