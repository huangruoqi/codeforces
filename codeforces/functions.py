import os
from .settings import *
space = '\n\t'
from .utils import (
    get_contest,
    create_folder,
    create_questions,
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
    if input("Enter `yes` to generate contest: ").lower().strip()!="yes":
        print("Exiting contest initialization...")
        return
    folder_path = create_folder(contest_name)
    create_questions(contest_id, questions, folder_path, contest_name)

    # README
    readme = open(os.path.join(folder_path, 'README.md'),'w')
    readme.write(f"# {contest_name}\n")
    readme.write(f"{url}\n")
    readme.close()
    
    