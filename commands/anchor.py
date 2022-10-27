import os
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator


def main():
    path = inquirer.filepath(
        default="./",
        message="Enter path to download:",
        validate=PathValidator(is_dir=True, message="Input is not a directory"),
        only_directories=True,
    ).execute()
    print(path)


if __name__ == "__main__":
    main()