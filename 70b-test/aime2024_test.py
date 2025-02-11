import requests
import json

url = "http://localhost:11434/api/generate"

version = ["32"]

f = open('../benchmark/AIME2024.txt', 'r')

lines = f.read()

question = list(lines.split("\n"))
question.pop()

headers = {"Content-Type": "application/json"}

for ver in version:
    model_name = "deepseek-r1:" + ver + "b"

    print(f'answers from {model_name}')

    answers = []

    for idx, quest in enumerate(question, start = 1):
        print(f"===================================question {idx}===================================")

        data = {
            "model": model_name,
            "prompt": quest
        }

        if not (data["prompt"] == quest):
            exit(1)

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print(f'Question: {data["prompt"]}')

            json_objects = response.content.decode().strip().split('\n')

            data = [json.loads(obj) for obj in json_objects]

            res_text = ''
            for item in data:
                res_text += item['response']

            print(res_text)

            print(f"===================================done===================================\n\n")

        else:
            print(f'Error: {response.status_code}, {response.text}')

    print(f'Testing {model_name} is done\n\n')
