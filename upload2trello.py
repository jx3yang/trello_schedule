import time
from typing import List

from data_models import *
from parsing import *
from trello_api import *

Credentials = TrelloCredentials

BOARD_FILE = 'board.yaml'
COURSES_FILE = 'courses.yaml'

def upload_course(credentials: Credentials, trello_board: TrelloBoard, trello_list: TrelloList, course: Course):
    course_name = course.name.upper()
    cards = [
        TrelloCard(
            name=f'{course_name} {work.title}',
            desc=f'Worth {work.percent_worth}%' if work.percent_worth is not None else None,
            due=work.due_date,
            start=work.start_date,
        )
        for work in course.assignments + course.quizzes + course.exams
    ]

    for card in cards:
        params = { 'name': card.name, 'desc': card.desc, 'due': card.due }
        response = create_card(credentials, trello_list.list_id, params)
        if response.status_code == 200 and card.start:
            card_id = json.loads(response.text)['id']
            field_value = { 'date': card.start }
            update_card_custom_field(credentials, card_id, trello_board.start_date_id, field_value)

def main():
    courses = parse_courses_file(COURSES_FILE)
    credentials = get_credentials()
    trello_board, trello_list = parse_board_file(credentials, BOARD_FILE)
    for course in courses:
        upload_course(credentials, trello_board, trello_list, course)
        # avoid hitting api call limit
        time.sleep(5)

if __name__ == '__main__':
    main()
