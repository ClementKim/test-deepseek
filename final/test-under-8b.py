import pandas as pd

from sys import argv
from transformers import pipeline

def ask_to_deepseek_r1(
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
    file_list = []

#    file_name = 
    model_number = argv[1]
    questions = file_to_list(file_name)

    for index, question in enumerate(questions, start = 1):
        ask_to_deepseek_r1(question, model_number)

if __name__ == "__main__":
    main()
