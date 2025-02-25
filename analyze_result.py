def file_to_list(file_dir : str) -> list:
    f = open(file_dir, "r")

    lines = f.read()

    listed_file = list(lines.split("\n"))

    return listed_file

def main():
    file_dir = "./result.txt"

    lst = file_to_list(file_dir)

    print(lst[-3])

if __name__ == "__main__":
    main()
