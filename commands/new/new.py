# check what prefers.
import os
import subprocess
import argparse
from InquirerPy import prompt
import json
import re
from prompt_toolkit.validation import ValidationError, Validator


def getUserInfo(validators: dict, templates: dict) -> dict:
    questions = [
        {
            "message": "Choose a template to load:",
            "choices": list(templates.keys()),
            "name": "template",
            "type": "list",
        },
        {
            "message": "Type the project folder name:",
            "type": "input",
            "name": "name",
            "validate": validators["ProjectNameValidator"],
        },
        {
            "message": "Enter github repo url:",
            "type": "input",
            "name": "repo_url",
            "validate": validators["GithubRepoValidator"],
        },
    ]

    info = prompt(questions, vi_mode=True)
    return info


def getExtraInfo(questions: list, validators: dict) -> dict:
    """propmts the user with the new data from the template config file

    Parameters
    ----------
    questions : list
        list of enw questions
    validators : dict
        list of custom validators for the questions

    Returns
    -------
    extra_info : dict
        extra_info required for the specific template
    """
    # check if there is project specific info:
    # extra_questions = #go to project and grab caravela.config.json
    # this part can be put in the template directly or something
    for q in questions:
        if "when" in q:
            q["when"] = add_condition(q["when"])
        if "validate" in q:
            q["validate"] = validators[q["validate"]]

    extra_info = prompt(questions, vi_mode=True)
    return extra_info


def fetchOnlineTemplate(template_dir: str, project_dir: str) -> dict:
    """Copies template dir to project_dir and fetches config

    Parameters
    ----------
    template_dir : string
        string with path of template directory
    project_dir : string
        string with path of project directory

    Returns
    -------
    config_info : dict
        dictionary containing contents of config file in template

    Raises
    ------
    OSError
        if teamplate directory does not exist
    """

    # raise error if it doesnt work
    # might need some sanitization of girhub url
    # degit #template_dir "project_dir"

    return config_info


def fetchOfflineTemplate(template_dir: str, project_dir: str) -> dict:
    """Copies template dir to project_dir and fetches config

    Parameters
    ----------
    template_dir : string
        string with path of template directory
    project_dir : string
        string with path of project directory

    Returns
    -------
    config_info : dict
        dictionary containing contents of config file in template

    Raises
    ------
    OSError
        if teamplate directory does not exist
    """

    if not os.path.exists(template_dir):
        raise OSError
    # get content file
    with open(template_dir + "/caravela.config.json", "r") as f:
        config_info = json.load(f)

    # copy files to new directory
    subprocess.call(["cp", "-a", template_dir, project_dir])

    return config_info


def colapsePlaceholders(project_dir: str, info: dict, files: list) -> None:
    """collapses the template placeholders with user-privded data

    Parameters
    ----------
    project_dir : string
        string containing directory of project
    info : dict
        dictionary with contents of user provided data
    files : list
        list of the names of files with palceholders. This lsit comes from the configuration file in the template project
    """

    pattern = "(\{\{ *caravela\.(\w*) *\}\})"
    # This should match only this: {{caravela.something}}

    # add a try with key error here
    def caravelaSub(match):
        if match.group(2) in info:
            if type(info[match.group(2)]) != str:
                return str(info[match.group(2)])
            else:
                return str(info[match.group(2)])
        else:
            return f"Template ERROR: no key: {match.group(2)}"

    for placeholder in files:
        # read file first
        with open(project_dir + "/" + placeholder, "r") as f:
            data = f.read()
        # overwrite with new data
        with open(project_dir + "/" + placeholder, "w") as f:
            f.write(re.sub(pattern, caravelaSub, data))


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


class ProjectNameValidator(Validator):
    def __init__(self, directory):
        self.directory = directory

    def validate(self, document):
        # check if its empty
        if not len(document.text) > 0:
            raise ValidationError(
                message="Input cannot be empty.",
                cursor_position=document.cursor_position,
            )
        if not bool(re.search("^[a-zA-Z0-9_+-]*$", document.text)):
            raise ValidationError(
                message="Invalid name. Only _,+ and - are allowed.",
                cursor_position=document.cursor_position,
            )

        projects_list = list(get_projects(self.directory))
        if document.text in projects_list:
            raise ValidationError(
                message="Project name already exists",
                cursor_position=document.cursor_position,
            )


class GithubRepoValidator(Validator):
    def validate(self, document):
        # check if its empty
        if not len(document.text) > 0:
            raise ValidationError(
                message="Input cannot be empty.",
                cursor_position=document.cursor_position,
            )
        if not re.match(r"^(https:\/\/github\.com\/.*git$)", document.text):
            raise ValidationError(
                message="Invalid URL. Currently only github is accepted",
                cursor_position=document.cursor_position,
            )


def createValidators(args: dict) -> dict:
    validators = {
        "ProjectNameValidator": ProjectNameValidator(args["dir"]),
        "GithubRepoValidator": GithubRepoValidator(),
    }
    return validators


def add_condition(str_phrase):
    def condition(result):
        subject, verb, obj = str_phrase
        if obj == "False":
            return not result[subject]
        if obj == "True":
            return result[subject]
        if verb == ">":
            return result[subject] > float(object)
        if verb == "<":
            return result[subject] < float(object)
        if verb == ">=":
            return result[subject] >= float(object)
        if verb == "<=":
            return result[subject] <= float(object)
        else:
            return result[subject] == obj

    return condition


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--pref")
    parser.add_argument("--dir")
    args = vars(parser.parse_args())

    validators = createValidators(args)
    with open("commands/new/templates.json", "r") as f:
        templates = json.load(f)

    ##get initial user info: name mostly
    info = getUserInfo(validators, templates)

    project_dir = (
        args["dir"] + "/" + templates[info["template"]]["type"] + "/" + info["name"]
    )

    ###### COPY FILES AND GRAB CONFIG FILE (TEMPLATE-INFO) #####
    if args["pref"] == "offline":
        try:
            config_info = fetchOfflineTemplate(
                templates[info["template"]]["offline_url"], project_dir
            )
        except OSError:
            print("Offline template not found -> grabbing online")

    if args["pref"] == "online":
        try:
            config_info = fetchOnlineTemplate(
                templates[info["template"]]["online_url"], project_dir
            )
        except OSError:
            print("Online template not found -> grabbing offline")

    ###### ASK USER FOR MORE INFO #########
    extra_info = getExtraInfo(questions=config_info["questions"], validators=validators)

    ##### MERGE THE TWO INFOS, give precendence to template #####
    info = info | extra_info

    ##### COLAPSE PLACEHOLDERS OF PROJECT ######
    colapsePlaceholders(
        project_dir=project_dir,
        info=info,
        files=config_info["placeholders"],
    )

    ######### RUN MAKE INIT #########
    subprocess.Popen(["make", "init"], stdout=subprocess.PIPE, cwd=project_dir)


if __name__ == "__main__":
    main()
