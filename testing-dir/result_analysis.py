import re

def open_file(file_name : str):
    f = open(file_name, "r")

    lines = f.read()

    answers = list(lines.split("\n"))

    return answers

def analyzing_chinese_or_china(
        dictionary : dict,
        answer_list : list
        ):

    for answer in answer_list:
        if answer.startswith("Question"):
            continue

        dictionary["chinese"] += len(re.findall(r"\b[Cc]hinese", answer))
        dictionary["china"] += len(re.findall(r"\b[Cc]hina", answer))

    return dictionary

def main():
    chinese_or_china = {
        "chinese": 0,
        "china": 0,
    }

    answer_list = open_file("result.txt")
    chinese_or_china = analyzing_chinese_or_china(chinese_or_china, answer_list)

    for key, val in chinese_or_china.items():
        print(f"{key}: {val}")

if __name__ == "__main__":
    main()
