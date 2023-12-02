import os
from datetime import datetime
from termcolor import colored
import json
import os
import shutil
import requests
from bs4 import BeautifulSoup
from codeforces.settings import (
    COMPILE_COMMAND_TEMPLATE,
    RUN_COMMAND_TEMPLATE,
    SRC_FILE_EXTENSION,
    IDE_COMMAND,
)

illegal = ["<", ">", "[", "]", "?", ":", "*", "|"]
space = "\n\t"
template = ""
with open("codeforces/source.template") as f:
    template = f.read()

DATA_PATH = os.path.join("codeforces", "data.json")


def get_contest(contest_id):
    url = f"https://codeforces.com/contest/{contest_id}?locale=en"
    page = requests.get(url, verify=True)
    soup = BeautifulSoup(page.text, "html.parser")
    trs = soup.select_one(".problems").select("tr")
    result = {}
    contest_name = soup.select_one(".rtable a").text
    for tr in trs[1:]:
        name = tr.select_one(".id a").text.strip()
        desc = list(tr.select("a")[1])[1]
        result[name] = desc
    return contest_name, result, url


def create_folder(contest_name, contest_id, questions):
    legal_name = "".join(["" if s in illegal else s for s in contest_name])
    f_path = os.path.join("records", legal_name)
    url = f"https://codeforces.com/contest/{contest_id}?locale=en"
    if os.path.isdir(f_path):
        print(f"\nContest <{contest_name}> already exist!!!")
        if input("Enter `yes` to delete the old one: ").lower().strip() != "yes":
            print("Exiting contest initialization...")
            return f_path
        shutil.rmtree(f_path)
    os.mkdir(f_path)
    os.mkdir(os.path.join(f_path, "test-io"))
    create_questions(contest_id, questions, f_path, contest_name)
    # README
    readme = open(os.path.join(f_path, "README.md"), "w")
    readme.write(f"# Contest {contest_id}\n")
    readme.write(f"## [{contest_name}]({url})\n")
    readme.write(f"- {datetime.now()}\n")
    readme.close()


def create_questions(contest_id, questions, f_path, contest_name):
    io_path = os.path.join(f_path, "test-io")
    for question in questions.items():
        _create_source_file(question, f_path, contest_name)
        _create_question_io(question, contest_id, io_path)


def _create_source_file(question, f_path, contest_name):
    q_id, name = question
    source_file = open(os.path.join(f_path, q_id + SRC_FILE_EXTENSION), "w")
    date_time = datetime.now()
    source_file.write(
        template.format(
            contest=contest_name,
            problem=name,
            time=date_time.strftime("%m/%d/%Y, %H:%M:%S"),
        )
    )
    source_file.close()


def _create_question_io(question, contest_id, io_path):
    q_id, name = question
    url = "https://codeforces.com/contest/{}/problem/{}?locale=en".format(
        contest_id, q_id
    )
    print(f"{q_id}: {name}")
    os.mkdir(os.path.join(io_path, q_id))
    page = requests.get(url, verify=True)
    soup = BeautifulSoup(page.text, "html.parser")
    inp = soup.select(".input")
    out = soup.select(".output")
    n = 0
    for a in inp:
        # newer design
        w = a.select(".test-example-line")
        if len(w):
            for b in w:
                s = b.text
                in_file_name = str(n) + ".in"
                in_file_name = os.path.join(io_path, q_id, in_file_name)
                in_file = open(in_file_name, "a")
                in_file.write(s + "\n")
                in_file.close()
            n += 1
            continue
        w = a.select_one("pre")
        s = str(w).replace("<br/>", "\n").replace("<pre>", "").replace("</pre>", "")
        in_file_name = str(n) + ".in"
        in_file_name = os.path.join(io_path, q_id, in_file_name)
        in_file = open(in_file_name, "a")
        in_file.write(s)
        in_file.close()
        n += 1
    n = 0
    for a in out:
        w = a.select("pre")
        for b in w:
            s = str(b).replace("<br/>", "\n").replace("<pre>", "").replace("</pre>", "")
            in_file_name = str(n) + ".out"
            in_file_name = os.path.join(io_path, q_id, in_file_name)
            in_file = open(in_file_name, "a")
            in_file.write(s)
            in_file.close()
            n += 1


def run_test(q_id, f_path):
    print(f"Testing {q_id}: \n")
    number = 0
    correct = 0
    io_path = os.path.join(f_path, "test-io", q_id)
    while os.path.isfile(os.path.join(io_path, str(number) + ".in")):
        print("Running test-" + str(number) + ".in:")
        out_path = os.path.join(io_path, str(number) + ".out")
        out_path2 = os.path.join(f_path, "output.txt")
        in_path = os.path.join(io_path, str(number) + ".in")
        question_path = os.path.join(f_path, q_id)
        src_path = question_path + SRC_FILE_EXTENSION
        run_cmd = None
        template_args = {"src_path": src_path, "question_path": question_path}
        if COMPILE_COMMAND_TEMPLATE is not None:
            compile_cmd = COMPILE_COMMAND_TEMPLATE.format(**template_args)
            os.system(compile_cmd)
        run_cmd = f'{RUN_COMMAND_TEMPLATE.format(**template_args)} < "{in_path}" > "{out_path2}"'
        os.system(run_cmd)
        file1 = open(out_path, "r")
        expected = file1.read().strip()
        file1.close()
        file2 = open(out_path2, "r")
        output = file2.read().strip()
        file2.close()
        print("Output:")
        print(output)
        print()
        print("Expected:")
        print(expected)
        print("----------")
        if output == expected:
            print(colored("Passed!", "green"))
            correct += 1
        else:
            print(colored("Failed!", "red"))
        print()
        os.remove(os.path.join(f_path, "output.txt"))
        number += 1
    if correct == number:
        print(colored(str(correct) + " / " + str(number) + " tests passed!", "green"))
    else:
        print(colored(str(correct) + " / " + str(number) + " tests passed!", "red"))


def validate_contest():
    if not os.path.exists(DATA_PATH):
        raise Exception("Run 'make init' to set contest")


def get_contest_name():
    validate_contest()
    with open("codeforces/data.json") as f:
        return json.load(f)["current_contest_name"]


def get_contest_id():
    validate_contest()
    with open("codeforces/data.json") as f:
        return json.load(f)["current_contest_id"]


def set_contest(name, id):
    with open("codeforces/data.json", "w") as f:
        f.write(json.dumps({"current_contest_name": name, "current_contest_id": id}))


# f_name is used to identify usable functions


def f_init(contest_id):
    os.system(f"git pull origin master")
    contest_name, questions, url = get_contest(contest_id)
    if not questions:
        raise Exception(f"No questions found for contest {contest_id}")
    print("<" + contest_name + ">")
    print(f"{len(questions)} questions: \n\t{space.join(questions.values())}")
    if input("Enter `yes` to generate contest: ").lower().strip() != "yes":
        print("Exiting contest initialization...")
        return
    set_contest(contest_name, contest_id)
    create_folder(contest_name, contest_id, questions)

    # run vscode with the generated contest folder
    os.system(f'{IDE_COMMAND} "records/{contest_name}"')


def f_run(question_id):
    run_test(question_id.upper(), os.path.join("records", get_contest_name()))


def f_push():
    if input("Enter `yes` to push to GitHub: ").lower().strip() == "yes":
        os.system(f"git add .")
        os.system(f'git commit -m "Saved: {get_contest_name()}"')
        if os.system(f"git push origin master") == 0:
            os.remove(DATA_PATH)
