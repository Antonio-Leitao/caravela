import os
import sys
from InquirerPy import prompt


def get_projects(projects_folder, templates=["C++", "Python", "Web"]):
    projects = {}
    for f in os.scandir(projects_folder):
        if not f.is_dir():
            continue

        if f.name not in templates:
            projects[f.name] = f.path
            continue

        for p in os.scandir(f.path):
            if p.is_dir():
                projects[p.name] = p.path

    return projects


def main():
    directory = sys.argv[1]
    projects = get_projects(directory)
    questions = [
        {
            "message": "What's our heading?",
            "type": "fuzzy",
            "choices": list(projects.keys()),
            "name": "heading",
        }
    ]
    result = prompt(questions, vi_mode=True)
    os.system("code {}".format(projects[result["heading"]]))


if __name__ == "__main__":
    main()
