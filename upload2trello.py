import yaml
from trello_api import *
from data_models import *

BOARD = 'board'
LIST = 'list'

COURSES = 'courses'
ASSIGNMENTS = 'assignments'
QUIZZES = 'quizzes'
EXAMS = 'exams'

ALL = 'all'
NUM = 'num'

NAME = 'name'
START = 'start'
DUE = 'due'
WORTH = 'worth'


def raise_fields_not_found(fields: list):
    quotes = lambda x: f'"{x}"'
    fields_strings = ', '.join(quotes(field) for field in fields)
    raise Exception(f'Requires {fields_strings} field(s)')

def verify_fields(fields: list, obj: dict):
    not_found = [field for field in fields if field not in obj]
    if len(not_found) > 0: raise_fields_not_found(not_found)

def load_board_info(file: str):
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
    verify_fields([BOARD, LIST], data)
    return data

def load_courses_info(file: str):
    with open(file, 'r') as f:
        data = yaml.safe_load(file)
    verify_fields([COURSES], data)
    return data
    

def main():
    board_info = load_board_info('board.yaml')
    board_name = board_info[BOARD]
    list_name = board_info[LIST]
    credentials = get_credentials()
    board_id = get_board_id(credentials, board_name)
    print(get_list_id(credentials, board_id, list_name))

if __name__ == '__main__':
    main()
