from transformers import pipeline

def ask_to_deepseek_r1(content, model_number):
    messages = [
        {"role": "user",
        "content": content}
    ]

    if not (content == messages["content"]):
#        return "error"

        print("Error")
        exit(1)

    pipe = pipeline("text-generation", model = "deepseek-ai/DeepSeek-R1-Distill-Llama-" + model_number + "B")
#    returned_message = pipe(messages)

    pipe(messages)

#    return returned_message

def txt_to_list(file_name):
    f = open(file_name, "r")

    lines = f.read()

    question = list(lines.split("\n"))
    question.pop()

    return question

def main():
    file_list = ["test", "../70b-test/political_question", "../benchmark/AIME2024", "../gre/gre_questions"]

    file_name = file_list[0] + ".txt"
    model_number = 70

    qustions = txt_to_list(file_name)

    for index, question in enumerate(questions, start = 1)
        print(f"====================question {index}====================")
#       msg = ask_to_deepseek_r1(question, model_number)
        ask_to_deepseek_r1(question, model_number)
        print(f"====================done for {index}====================")

        '''
        if not (msg == "error"):
            answer = list(msg.split("\n"))

            if answer[-1] == "\\]":
                answer = answer[-2]


        else:
            print("Error in code")
            exit(1)
        '''

if __name__ == "__main__":
    main()
