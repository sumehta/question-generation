import sys
import argparse
from question_generator import QuestionGenerator


def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '-sentence', type=str, help="The sentence for which questions are to be generated.")
    parser.add_argument('-t', '-question_type', type=str, default='Wh', choices=['Wh', 'Are'], help='The types of questions to be generated.')
    return parser.parse_args()


if __name__ == '__main__':
    args = add_arguments()
    if not args.s:
        sys.stdout.write('No input given\n')
        sys.exit()
    q  = QuestionGenerator()
    question_list = q.generate_question(args.s, [args.t])
    for questions in question_list:
        for question in questions:
            sys.stdout.write(question)
            sys.stdout.write("\n")
