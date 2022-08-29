import os
from .settings import *

space = "\n\t"
from .utils import (
    get_contest,
    create_folder,
    create_questions,
    run_test,
    set_contest_name,
    get_contest_name,
)

# f_name is used to identify usable functions


def f_setup():
    print("setup")
    pass


def f_init(contest_id):
    contest_name, questions, url = get_contest(contest_id)
    if not questions:
        raise Exception(f"No questions found for contest {contest_id}")
    print(f"{len(questions)} questions: \n\t{space.join(questions.values())}")
    if input("Enter `yes` to generate contest: ").lower().strip() != "yes":
        print("Exiting contest initialization...")
        return
    folder_path = create_folder(contest_name)
    set_contest_name(contest_name)
    create_questions(contest_id, questions, folder_path, contest_name)

    # README
    readme = open(os.path.join(folder_path, "README.md"), "w")
    readme.write(f"# {contest_name}\n")
    readme.write(f"{url}\n")
    readme.close()


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
