import requests
import pickle
import json

from datasets import load_dataset

ds = load_dataset("cais/mmlu", "all")

mmlu_test = ds['test']
mmlu_val = ds['validation']
mmlu_dev = ds['dev']
mmlu_aux = ds['auxiliary_train']

mmlu_test_question = mmlu_test[:]['question']
mmlu_test_choices = mmlu_test[:]['choices']

mmlu_val_question = mmlu_val[:]['question']
mmlu_val_choices = mmlu_val[:]['choices']

mmlu_dev_question = mmlu_dev[:]['question']
mmlu_dev_choices = mmlu_dev[:]['choices']

mmlu_aux_question = mmlu_aux[:]['question']
mmlu_aux_choices = mmlu_aux[:]['choices']

mmlu_test_question = [i.replace("\n", " ") for i in mmlu_test_question]
mmlu_test_choices = [[choice.replace("\n", " ") for choice in choices] for choices in mmlu_test_choices]

mmlu_test_question_plus_choices = [
    mmlu_test_question[i] + " " + "The choices are as follows: " + " ".join(mmlu_test_choices[i])
    for i in range(len(mmlu_test_question))
]

mmlu_val_question_plus_choices = [
    mmlu_val_question[i] + " " + "The choices are as follows: " + " ".join(mmlu_val_choices[i])
    for i in range(len(mmlu_val_question))
]

mmlu_dev_question_plus_choices = [
    mmlu_dev_question[i] + " " + "The choices are as follows: " + " ".join(mmlu_dev_choices[i])
    for i in range(len(mmlu_dev_question))
]

mmlu_aux_question_plus_choices = [
    mmlu_aux_question[i] + " " + "The choices are as follows: " + " ".join(mmlu_aux_choices[i])
    for i in range(len(mmlu_aux_question))
]

url = "http://localhost:11434/api/generate"
version = "70"

headers = {"Content-Type": 'application/json'}

mmlu_lst = [mmlu_test_question_plus_choices,
            mmlu_val_question_plus_choices,
            mmlu_dev_question_plus_choices,
            mmlu_aux_question_plus_choices]

print(len((mmlu_test_question_plus_choices)))
exit(1)

number_dictionary = {
        '0': 'test',
        '1': 'validation',
        '2': 'dev',
        '3': 'auxiliary train'
}

model_name = "deepseek-r1:" + version + "b"
print(f"answers from {model_name}")

integrated_answer = {
        'test':[],
        'validation': [],
        'dev': [],
        'auxiliary train': []
}

for number, mmlu in enumerate(mmlu_lst):
    print(f'the operation is on {number_dictionary[str(number)]}')

    if number:
        continue

    answers = []
    for idx, question in enumerate(mmlu, start = 1):
        print(f"====================Q{idx}====================")

        data = {
            "model": model_name,
            "prompt": question
        }

        if not (data["prompt"] == question):
            exit(1)

        response = requests.post(url, json = data, headers = headers)

        if response.status_code == 200:
#            print(f'Question: {data["prompt"]}')

            json_objects = response.content.decode().strip().split('\n')

            data = [json.loads(obj) for obj in json_objects]

            res_text = ''
            for item in data:
                res_text += item['response']

            answers.append(res_text)

            print("====================done====================\n\n")

        else:
            print(f"Error: {response.status_code}, {response.text}")

    for idx, sentences in enumerate(answers, start = 1):
        temp = list(sentences.split("\n"))

        if temp[-1] == "\\]":
            temp = temp[-2]
        integrated_answer[number_dictionary[str(number)]].append([idx, temp])

try:
    with open('result.pickle', 'wb') as fw:
        pickle.dump(integrated_answer, fw)

    print(f"Testing {model_name} is done \n\n")

except:
    print("Error: failed to save integrated answer")
