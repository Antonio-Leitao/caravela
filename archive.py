from InquirerPy import prompt
from InquirerPy.exceptions import InvalidArgument
from InquirerPy.validator import PathValidator


def is_upload(result):
    return result[0] == "Upload"


questions = [
    {
        "message": "Select an S3 action:",
        "type": "list",
        "choices": ["Upload", "Download"],
    },
    {
        "message": "Enter the filepath to upload:",
        "type": "filepath",
        "when": is_upload,
        "validate": PathValidator(),
        "only_files": True,
    },
    {
        "message": "Select a bucket:",
        "type": "fuzzy",
        "choices": ["CDN", "PLT", "GDS", "DSS", "PLJ", "GHS", "ZZZ", "HJG", "JHJ"],
        "name": "bucket",
    },
    {
        "message": "Select files to download:",
        "type": "fuzzy",
        "when": lambda _: not is_upload(_),
        "choices": ["CDN", "PLT", "GDS", "DSS", "PLJ", "GHS", "ZZZ", "HJG", "JHJ"],
        "multiselect": True,
    },
    {
        "message": "Enter destination folder:",
        "type": "filepath",
        "when": lambda _: not is_upload(_),
        "only_directories": True,
        "validate": PathValidator(),
    },
    {"message": "Confirm?", "type": "confirm", "default": False},
]


if __name__ == "__main__":
    result = prompt(questions, vi_mode=True)
    print(result)
