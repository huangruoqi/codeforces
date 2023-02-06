from datetime import datetime
from termcolor import colored
import json
import os
import shutil
import requests
from bs4 import BeautifulSoup
import os

illegal = ["<", ">", "[", "]", "?", ":", "*", "|"]
f = open("codeforces/template.py")
template = f.read()
f.close()


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


def create_folder(name):
    legal_name = "".join(["" if s in illegal else s for s in name])
    f_path = os.path.join("records", legal_name)
    if os.path.isdir(f_path):
        print(f"\nContest <{name}> already exist!!!")
        if input("Enter `yes` to delete the old one: ").lower().strip() != "yes":
            print("Exiting contest initialization...")
            return
        shutil.rmtree(f_path)
    os.mkdir(f_path)
    os.mkdir(os.path.join(f_path, "test-io"))
    return f_path


def create_questions(contest_id, questions, f_path, contest_name):
    io_path = os.path.join(f_path, "test-io")
    for question in questions.items():
        _create_source_file(question, contest_id, f_path, contest_name)
        _create_question_io(question, contest_id, io_path)


def _create_source_file(question, contest_id, f_path, contest_name):

    q_id, name = question
    url = "https://codeforces.com/contest/{}/problem/{}?locale=en".format(
        contest_id, q_id
    )
    source_file = open(os.path.join(f_path, q_id + ".py"), "w")
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
        outPath = os.path.join(io_path, str(number) + ".out")
        outPath2 = os.path.join(f_path, "output.txt")
        inPath = os.path.join(io_path, str(number) + ".in")
        srcPath = os.path.join(f_path, q_id + ".py")
        cmd = f'poetry run python "{srcPath}" < "{inPath}" > "{outPath2}"'
        os.system(cmd)
        file1 = open(outPath, "r")
        expected = file1.read().strip()
        file1.close()
        file2 = open(outPath2, "r")
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


def get_contest_name():
    with open("codeforces/data.json") as f:
        return json.load(f)["current_contest_name"]


def get_contest_id():
    with open("codeforces/data.json") as f:
        return json.load(f)["current_contest_id"]


def set_contest(name, id):
    with open("codeforces/data.json", "w") as f:
        f.write(json.dumps({"current_contest_name": name, "current_contest_id": id}))
