import os
import argparse
from InquirerPy import prompt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--names', nargs='+')
    parser.add_argument('--locations', nargs='+')
    args = parser.parse_args()
    servers = vars(args)


    sails = {}
    for name,loc in zip(servers['names'], servers['locations']):
        sails[name]=loc
    

    questions = [
        {
            "message": "What's our heading?",
            "type": "fuzzy",
            "choices": list(sails.keys()),
            "name": "heading",
        }
    ]

    result = prompt(questions, vi_mode=True)  
    os.system("{}".format(sails[result['heading']]))


if __name__ == "__main__":
    main()
