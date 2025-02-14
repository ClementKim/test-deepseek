import requests
import json
import re

import pandas as pd

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

    return listed_file

def run_model(
        model_number : int,
        question_list : list
        ) -> list:

    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    model_name = "deepseek-r1:" + str(model_number) + "b"

    returned_respond = []
    for idx, question in enumerate(question_list, start = 1):
        print(f"now solving Q{idx}")

        data = {
            "model": model_name,
            "prompt": question
        }

        if not (data["prompt"] == question):
            print(f"Error in data prompt: question numer {idx}")
            exit(1)

        response = requests.post(url, json = data, headers = headers)

        if response.status_code == 200:
            json_objects = response.content.decode().strip().split("\n")
            data = [json.loads(obj) for obj in json_objects]

            res_text = ''
            for item in data:
                res_text += item['response']

            returned_respond.append(res_text)

        else:
            print("Error: {response.status_code}, {response.text}")

    return returned_respond

def split_answer_thinking(model_result : list) -> tuple[list, list]:
    answer_only = []
    thinking_only = []

    for index, sentences in enumerate(model_result, start = 1):
        sentence_split = list(sentences.split("\n"))

        thinking = False
        thinking_temp_list = []
        for think_process in sentence_split:
            if "<think>" in think_process:
                thinking = True
                continue

            elif "</think>" in think_process:
                break

            if thinking:
                thinking_temp_list.append(think_process)


        thinking_only.append(thinking_temp_list)

        if sentence_split[-1] == "\\]":
            boxed_answer = sentence_split[-2]
        else:
            boxed_answer = sentence_split[-1]

        answer_only.append(boxed_answer)

    return answer_only, thinking_only

def find_word_china_and_chinese(thinking_only : list) -> dict:
    china_or_chinese = {
        "chinese" : 0,
        "china" : 0
    }

    for thinking_list in thinking_only:
        for think in thinking_list:
            china_or_chinese["chinese"] += len(re.findall(r"\b[Cc]hinese", think))
            china_or_chinese["china"] += len(re.findall(r"\b[Cc]hina", think))

    return china_or_chinese

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


def matching_answer(
        answer_list : list,
        model_result_list : list
        ) -> int:

    number_of_matching = 0
    actual_returned_answer = []

    for sentence in model_result_list:
        for index in range(len(sentence)-1, 7, -1):
            if sentence[index-7:index] == "\\boxed{":
                anchor = 0
                while sentence[index+anchor] != "}":
                    anchor += 1

                actual_returned_answer.append(sentence[index:index+anchor])

    if not (len(actual_returned_answer) == len(answer_list)):
        print("Error: the length of actual returned answer and answer list are not matching")
        return -1

    for index in range(len(answer_list)):
        if (int(answer_list[index]) == int(actual_returned_answer[index])):
            number_of_matching += 1

    return number_of_matching


def main():
    question_and_answer_dir = [
        # [file name, result is number or string, question is related with politics, answer file (if the result is number)] 
#        ["questions/sample_question.txt", "string", False],
        ["benchmark/gpqa_diamond.csv", "string", False]
#        ["benchmark/aime/2024/AIME2024.txt", "number", False, "benchmark/aime/2024/AIME2024-answer.txt"],
#        ["benchmark/gre/gre-questions.txt", "string", False],
#        ["questions/political_question.txt", "string", True],
#        ["questions/question_logic.txt", "number", False, "questions/question_logic-answer.txt"],
#        ["questions/question_not_logic.txt", "string", False]
    ]

    model_to_run = [70]
    returned_result = {}

    for testing_target in question_and_answer_dir:
        questions = file_to_list(testing_target[0])

        returned_result[testing_target[0]] = {}

        for model_number in model_to_run:
            result_to_append = []

            returned_respond = run_model(model_number, questions)

            respond_answer, think = split_answer_thinking(returned_respond)
            speak_chinese, number_of_chinese, error_list = find_speak_chinese(returned_respond)

            result_to_append.extend([speak_chinese, number_of_chinese, error_list, testing_target[2]])

            if not (testing_target[2]):
                mentioning_china_or_chinese_while_thinking = find_word_china_and_chinese(think)
                result_to_append.append(mentioning_china_or_chinese_while_thinking)

            else:
                result_to_append.append({})

            if testing_target[1] == "number":
                answers = file_to_list(testing_target[3])
                number_of_matching = matching_answer(answers, respond_answer)
                result_to_append.append(number_of_matching)

            else:
                result_to_append.append(respond_answer)

            returned_result[testing_target[0]][model_number] = result_to_append

    for idx, target_key in enumerate(question_and_answer_dir, start = 1):
        for key, value in returned_result[target_key[0]].items():
            save_file = "result/"+ target_key[0][:-4] + "_" + str(key) + "_result.txt"

            with open(save_file, "w") as file:
                file.write("speaking Chinese: " + str(value[0]) + "\n")
                file.write("number of chinese: " + str(value[1]) + "\n")

                file.write("error sentences: \n")
                for sentence in value[2]:
                    file.write(sentence + " ")

                file.write("\n")

                if not (value[3]):
                    file.write('number of mentioning the word "Chinese" while thinking: ' + str(value[4]['chinese']) + "\n")
                    file.write('number of mentioning the word "China" while thinking: ' + str(value[4]['china']) + "\n")

                if (target_key[1] == "number"):
                    file.write("number of corrects: " + str(value[5] + "\n"))

                else:
                    file.write("returned responds: \n")
                    for idx, respond in enumerate(value[5], start = 1):
                        file.write("Q" + idx + ":")
                        file.write(respond + "\n")

            file.close()

if __name__ == "__main__":
    main()
