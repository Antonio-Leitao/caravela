from InquirerPy import prompt


def main():
    questions = [
        {
            "message": "What are we to do?",
            "type": "fuzzy",
            "choices": ['new','goto','sail','anchor','port'],
            "name": "action",
        }
    ]
    result = prompt(questions, vi_mode=True)
    print(result['action'])


if __name__ == "__main__":
    main()

