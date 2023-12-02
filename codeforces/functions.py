import os
from .utils import (
    DATA_PATH,
    get_contest,
    create_folder,
    run_test,
    set_contest,
    get_contest_name,
)

space = "\n\t"
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
    os.system(f'code "records/{contest_name}"')


def f_run(question_id):
    run_test(question_id.upper(), os.path.join("records", get_contest_name()))


def f_push():
    if input("Enter `yes` to push to GitHub: ").lower().strip() == "yes":
        os.system(f"git add .")
        os.system(f'git commit -m "Saved: {get_contest_name()}"')
        if os.system(f"git push origin master") == 0:
            os.remove(DATA_PATH)
