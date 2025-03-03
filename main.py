import pickle
import requests
import json
import re

import pandas as pd

from sys import argv
from transformers import pipeline, AutoTokenizer

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
        raise ValueError(f"Invalid File Type Error : '{file_dir[-4:]}' is not a correct file type")

    return listed_file

def run_model(
        model_number : str,
        model_version : str,
        question_list : list,
        ) -> list:

    if (model_version == "full"):
        qwen = ["1.5", "7", "14", "32"]
        llama = ["8", "70"]

        if (model_number in qwen):
            model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-" + model_number + "B"

        elif (model_number in llama):
            model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-" + model_number + "B"

        else:
            raise ValueError(f"Model Number Error : '{model_number}' is not a correct model number")

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if (tokenizer.model_max_length == None):
            raise ValueError(f"Error : '{tokenizer.model_max_length}' is not a correct max length of model")

        pipe = pipeline("text-generation",
                model = model_name,
                device_map = "auto"
                )

    elif (model_version == "quantized"):
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        model_name = "deepseek-r1:" + model_number + "b"

    else:
        raise ValueError(f"Invalid Model Version : {model_version}")

    full_answer = []
    for question_number, question in enumerate(question_list, start = 1):
        print(f"now solving Q{question_number}")

        if (model_version == "full"):
            full_answer.append(list(pipe(question,
                            max_length = tokenizer.model_max_length,
                            do_sample = True,
                            truncation = True)))

        elif (model_version == "quantized"):
            data = {
                "model": model_name,
                "prompt": question
            }

            response = requests.post(url, json = data, headers = headers)

            if (response.status_code == 200):
                json_objects = response.content.decode().strip().split("\n")
                data = [json.loads(obj) for obj in json_objects]

                res_text = ''
                for item in data:
                    res_text += item['response']

                full_answer.append(res_text)

            else:
                raise ValueError(f"Error : {response.status_code}, {response.text}")

    print("running model is done")

    return full_answer

def split_answer_thinking(
        model_version : str,
        model_result : list
        ) -> tuple[list, list]:

    answer_only = []
    thinking_only = []

    for sentence in model_result:
        if (model_version == "full"):
            sentence_split = list(sentence[0]['generated_text'].split("\n"))

        elif (model_version == "quantized"):
            sentence_split = list(sentence.split("\n"))

        thinking_temp_list = []
        for thinking_process in sentence_split:
            if "</think>" in thinking_process:
                break

            thinking_temp_list.append(thinking_process)

    thinking_only.append(thinking_temp_list)

    if (sentence_split[-1] == "\\]"):
        boxed_answer = sentence_split[-2]
    else:
        boxed_answer = sentence_split[-1]

    answer_only.append(boxed_answer)

    return answer_only, thinking_only
'''
    elif (model_version == "quantized"):
        for sentences in model_result:
            sentence_split = list(sentences.split("\n"))

            thinking = False
            thinking_temp_list = []
            for thinking_process in sentence_split:
                if "<think>" in thinking_process:
                    thinking = True
                    continue

                elif "</think>" in thinking_process:
                    break

                if (thinking):
                    thinking_temp_list.append(thinking_process)

            thinking_only.append(thinking_temp_list)

            if (sentence_split[-1] == "\\]"):
                boxed_answer = sentence_split[-2]
            else:
                boxed_answer = sentence_split[-1]

            answer_only.append(boxed_answer)
'''

def find_word_china_and_chinese(thinking_only : list) -> dict:
    china_or_chinese = {
        "chinese": 0,
        "china": 0
    }

    for thinking_list in thinking_only:
        for think in thinking_list:
            china_or_chinese['chinese'] += len(re.findall(r"\b[Cc]hinese", think))
            china_or_chinese['china'] += len(re.findall(r"\b[Cc]hina", think))

    return china_or_chinese

def find_speak_chinese(
        model_version : str,
        respond_list : list
        ) -> tuple[bool, int, list]:
    number_of_chinese = 0
    speak_chinese = False

    errors_list = [] # temporal list for checking error or not
    ascii_list = [str(ascii_number) for ascii_number in range(128)]

    for answer in respond_list:
        if (model_version == "full"):
            answer = answer[0]['generated_text']

        for letter in answer:
            if not (str(ord(letter)) in ascii_list):
                number_of_chinese += 1
                errors_list.append(letter)

    if number_of_chinese:
        speak_chinese = True

    return speak_chinese, number_of_chinese, errors_list

def main():
    question_and_answer_dir = [
        # [file name, result is number or string, question is related with politics, answer file (if the result is number)]
        ["questions/sample_question.txt", "string", False],
#        ["questions/sample_question2.txt", "string", False]
#        ["benchmark/gpqa/gpqa_diamond.pkl", "string", False, None],
#        ["benchmark/aime/2024/AIME2024.txt", "string", False, None],
#        ["benchmark/gre/gre-questions.txt", "string", False],
#        ["questions/political_question.txt", "string", True],
#        ["questions/question_logic.txt", "string", False, "questions/question_logic-answer.txt"],
#        ["questions/question_not_logic.txt", "string", False],
#        ["benchmark/aime/2025/AIME2025.txt", "string", False, None],
#        ["benchmark/math500/problem_set.pkl", "string", False, None]
    ]

    # To run this program : python3 main.py [model_number] [model_version]
    # model_version: "full" for full precision, "quantized" for 4bit quantized

    model_number = argv[1]
    model_version = argv[2]

    returned_result = {}

    for testing_target in question_and_answer_dir:
        questions = file_to_list(testing_target[0])

        returned_result[testing_target[0]] = {}

        result_to_append = []

        returned_respond = run_model(model_number, model_version, questions)

        respond_answer, think = split_answer_thinking(model_version, returned_respond)
        speak_chinese, number_of_chinese, error_list = find_speak_chinese(model_version, returned_respond)

        result_to_append.extend([speak_chinese, number_of_chinese, error_list, testing_target[2]])

        mentioning_china_or_chinese_while_thinking = find_word_china_and_chinese(think)
        result_to_append.append(mentioning_china_or_chinese_while_thinking)

        result_to_append.append(respond_answer)

        returned_result[testing_target[0]][model_number] = result_to_append

    for idx, target_key in enumerate(question_and_answer_dir, start = 1):
        for key, value in returned_result[target_key[0]].items():
            if (model_version == "full"):
                file_name = "result/"+ target_key[0][:-4] + "_" + str(key) + "B_four_full_precision_result.txt"

            elif (model_version == "quantized"):
                file_name = "result/"+ target_key[0][:-4] + "_" + str(key) + "B_four_bit_quantized_result.txt"

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
