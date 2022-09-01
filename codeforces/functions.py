import os
import getpass
from .utils import (
    get_contest,
    create_folder,
    create_questions,
    run_test,
    set_contest,
    get_contest_name,
    get_contest_id,
    submit_question,
)

space = "\n\t"
# f_name is used to identify usable functions


def f_setup():
    n = input("What is your name    : ")
    e = input("What is your CF email: ")
    p = getpass.getpass("What is your password: ")
    o = input("GitHub repo URL      : ")
    os.system("git remote remove origin")
    os.system(f"git remote add origin {o}")
    settings = open("codeforces/settings.py", "w")
    settings.write(
        f"""
NAME = "{n}"
EMAIL = "{e}"
PASSWORD = "{p}"
URL = "{o}"
"""
    )
    settings.close()


def f_init(contest_id):
    contest_name, questions, url = get_contest(contest_id)
    if not questions:
        raise Exception(f"No questions found for contest {contest_id}")
    print("<" + contest_name + ">")
    print(f"{len(questions)} questions: \n\t{space.join(questions.values())}")
    if input("Enter `yes` to generate contest: ").lower().strip() != "yes":
        print("Exiting contest initialization...")
        return
    folder_path = create_folder(contest_name)
    set_contest(contest_name, contest_id)
    create_questions(contest_id, questions, folder_path, contest_name)

    # README
    readme = open(os.path.join(folder_path, "README.md"), "w")
    readme.write(f"# {contest_name}\n")
    readme.write(f"{url}\n")
    readme.close()

    # run vscode with the generated contest folder
    os.system(f'code "records/{contest_name}"')


def f_run(question_id):
    run_test(question_id.upper(), os.path.join("records", get_contest_name()))


def f_push():
    cmd = f'git commit -m "Finish {get_contest_name()}"'
    os.system(cmd)
    if input("Enter `yes` to push to GitHub: ").lower().strip() != "yes":
        print("Undoing lasest commit...")
        os.system("git reset --soft HEAD~1")
        return
    os.system("git push origin master")


def f_submit(question_id):
    submit_question(get_contest_name(), get_contest_id(), question_id)
