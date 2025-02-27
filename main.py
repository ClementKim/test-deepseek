import pickle
import requests
import json

import pandas as pd

from sys import argv
from transformers import pipeline

def file_to_list(file_dir : str) -> list:
    if (file_dir[-4:] == ".csv"):
        df = pd.read_csv(file_dir)

        question = df.loc[:, "Question"]

        listed_file = []
        for q in question:
            if q == "\n":
                continue

            listed_file.append(q)

    elif (file_dir[-4:] == ".txt"):
        f = open(file_dir, "r")

        lines = f.read()

        listed_file = list(lines.split("\n"))
        listed_file.pop()

        f.close()

    elif (file_dir[-4:] == ".pkl"):
        with open(file_dir, "rb") as f:
            listed_file = pickle.load(f)

    else:
        print("file type error")
        exit(1)

    return listed_file

def run_full_precision_model(
        model_number : str
        question_list : list,
        ) -> list:

    generated_answer = []

    pipe = pipeline("text-generation",
            model = "deepseek-ai/DeepSeek-R1-Distill-Llama-" + model_number + "B",
            device_map = "auto"
            )

    for question_number, question in enumerate(question_list, start = 1):
        print(f"now solving Q{question_number}")
        if (not (question)):
            break

        generated_answer.append(list(pipe(question,
                        max_length = 131072,
                        do_sample = True,
                        truncation = True)))

    print("done")

    full_answer = []
    for generated in range(len(generated_answer)):
        full_answer.append([target_dir[0], temp])

    return full_answer

def run_four_bit_quantized_model(
        model_number : str,
        question_list : list
        ) -> list:

    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    model_name = "deepseek-r1:" + model_number + "b"

    full_answer = []
    for question_number, question in enumerate(question_list, start = 1):
        print(f"now solvign Q{question_number}")

        data = {
            "model": model_name,
            "prompt": question
        }

        if not (data["prompt"] == question):
            print(f"Error in data prompt: question number {question_number}")
            exit(1)

        response = requests.post(url, json = data, headers = headers)

        if response.status_code = 200:
            json_objects = response.content.decode().strip().split("\n")
            data = [json.loads(obj) for obj in json_objects]

            res_text = ''
            for item in data:
                res_text += item['response']

            full_answer.append(res_text)

        else:
            print(f"Error: {response.status_code}, {response.text}")

    return full_answer

def split_answer_thinking(model_result : list) -> tuple[list, list]:
    '''
    code implementation for full precision is needed
    '''

    answer_only = []
    thinking_only = []

    for sentences in model_result:
        sentence_split = list(sentences.split("\n"))

        thinking = False
        thinking_temp_list = []
        for thinking_process in sentence_split:
            if "<think>" in think_process:
                thinking = True
                continue

            elif "</think>" in think_process:
                break

            if (thinking):
                thinking_temp_list.append(think_process)

        thinking_only.append(thinking_temp_list)

        if (sentence_split[-1] == "\\]":
            boxed_answer = sentence_split[-2]
        else:
            boxed_answer = sentence_split[-1]

        answer_only.append(boxed_answer)

    return answer_only, thinking_only

def find_speak_chinese(respond_list : list) -> tuple[bool, int, list]:
    number_of_chinese = 0
    speak_chinese = False

    errors_list = [] # temporal list for checking error or not
    ascii_list = [str(ascii_number) for ascii_number in range(128)]

    for answer in respond_list:
        for letter in answer:
            if not (str(ord(letter)) in ascii_list):
                number_of_chinese += 1
                errors_list.append(letter)

    if not (number_of_chinese):
        speak_chinese = True

    return speak_chinese, number_of_chinese, errors_list

def main():
    question_and_answer_dir = [
        # [file name, result is number or string, question is related with politics, answer file (if the result is number)]
#        ["questions/sample_question.txt", "string", False],
#        ["questions/sample_question2.txt", "string", False]
        ["benchmark/gpqa/gpqa_diamond.pkl", "string", False, None],
        ["benchmark/aime/2024/AIME2024.txt", "string", False, None],
#        ["benchmark/gre/gre-questions.txt", "string", False],
#        ["questions/political_question.txt", "string", True],
#        ["questions/question_logic.txt", "string", False, "questions/question_logic-answer.txt"],
#        ["questions/question_not_logic.txt", "string", False],
        ["benchmark/aime/2025/AIME2025.txt", "string", False, None],
        ["benchmark/math500/problem_set.pkl", "string", False, None]
    ]

    # user input form: model_to_run,full_or_quantized
    # full_or_quantized: 1 for full precision, 0 for 4bit quantized
    user_ipt_list = list(argv[1].split(","))

    model_number = user_ipt_list[0]
    full_or_quantized = int(user_ipt_list[1])

    returned_result = {}

    for testing_target in question_and_answer_dir:
        questions = file_to_list(testing_target[0])

        returned_result[testing_target[0]] = {}

        result_to_append = []

        if (full_or_quantized):
            returned_respond = run_full_precision_model(model_number, questions)
        else:
            returned_respond = run_four_bit_quantized_model(model_number, questions)

        respond_answer, think = split_answer_thinking(returned_respond)
        speak_chinese, number_of_chinese, error_list = find_speak_chinese(returned_respond)

        result_to_append.extend([speak_chinese, number_of_chinese, error_list, testing_target[2]])

        if not (testing_target[2]):
            mentioning_china_or_chinese_while_thinking = find_word_china_and_chinese(think)
            result_to_append.append(mentioning_china_or_chinese_while_thinking)

        else:
            result_to_append.append({})

        result_to_append.append(respond_answer)

        returned_result[testing_target[0]][model_number] = result_to_append

    for idx, target_key in enumerate(question_and_answer_dir, start = 1):
        for key, value in returned_result[target_key[0]].items():
            if (full_or_quantized):
                file_name = "result/"+ target_key[0][:-4] + "_" + str(key) + "B_four_full_precision_result.txt"
            else:
                file_name = "result/"+ target_key[0][:-4] + "_" + str(key) + "B_four_bit_quanrized_result.txt"

            with open(file_name, "w") as file:
                file.write("speaking Chinese: " + str(value[0]) + "\n")
                file.write("number of chinese: " + str(value[1]) + "\n")

                file.write("error sentences: \n")
                for sentence in value[2]:
                    file.write(sentence + " ")

                file.write("\n")

                if not (value[3]):
                    file.write('number of mentioning the word "Chinese" while thinking: ' + str(value[4]['chinese']) + "\n")
                    file.write('number of mentioning the word "China" while thinking: ' + str(value[4]['china']) + "\n")

                file.write("returned responds: \n")
                for idx, respond in enumerate(value[5], start = 1):
                    file.write("Q" + str(idx) + ":")
                    file.write(respond + "\n\n")

            file.close()

if __name__ == "__main__":
    main()
