def file_to_list(file_dir : str) -> list:
    f = open(file_dir, "r")

    lines = f.read()

    listed_file = list(lines.split("\n"))

    generated_answer = []
    for question_number, sentence in enumerate(listed_file, start = 1):
        temp = ""
        flag = False

        for index in range(len(sentence)-6, 6, -1):
            if (sentence[index-6:index] == "Answer"):
                temp = sentence[index:]
                break

        if (temp):
            generated_answer.append([question_number, temp])

    f.close()

    if (not (generated_answer)):
        print("error on gerated answer")
        exit(1)

    return generated_answer



def main():
    file_dir = "./result.txt"

    generated_answer = file_to_list(file_dir)

    with open("answer_only.txt", "w") as file:
        for answer in generated_answer:
            file.write('question number ' + str(answer[0]) + " :\n")
            file.write(answer[1])
            file.write("\n\n")

        file.close()

if __name__ == "__main__":
    main()
