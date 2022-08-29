from datetime import datetime
import os
import shutil
import requests
from bs4 import BeautifulSoup
from .settings import *

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
            name=NAME,
            contest=contest_name,
            problem=name,
            time=date_time.strftime("%m/%d/%Y, %H:%M:%S"),
            url=url,
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
        w = a.select("pre")
        for b in w:
            s = str(b).replace("<br/>", "\n").replace("<pre>", "").replace("</pre>", "")
            in_file_name = str(n) + ".in"
            in_file_name = os.path.join(io_path, q_id, in_file_name)
            in_file = open(in_file_name, "a")
            in_file.write(s[1:])
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
            in_file.write(s[1:])
            in_file.close()
            n += 1
