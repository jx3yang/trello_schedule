from .utils import load_board_info, load_courses_info, not_found_fields, verify_fields
from .constants import *

from data_models import *
from trello_api import get_board_id, get_list_id
from time_utils import get_date

from typing import List, Optional, Tuple, Type

Credentials = TrelloCredentials

def parse_board_file(credentials: Credentials, file: str) -> Optional[Tuple[TrelloBoard, TrelloList]]:
    board_info = load_board_info(file)
    board_name = board_info[BOARD]
    list_name = board_info[LIST]
    start_date_field = board_info[START_DATE_FIELD]
    board_id = get_board_id(credentials, board_name)
    list_id = get_list_id(credentials, board_id, list_name)

    trello_board = TrelloBoard(board_id=board_id, name=name, start_date_field=start_date_field)
    trello_list = TrelloList(list_id=list_id, name=list_name)
    return trello_board, trello_list


def parse_class_work_group(data: dict, prefix: str, idx: int, course_name: str, WorkType: Type[ClassWork]) -> Optional[List[ClassWork]]:
    verify_fields([ALL], data)
    data_all = data[ALL]
    verify_fields([NUM], data_all)
    num = data_all[NUM]

    def _get_date(field: str, i: int):
        has_not_found, not_found = not_found_fields([field, FREQUENCY], data_all)
        if has_not_found:
            if field in not_found: return None
            if FREQUENCY in not_found: return get_date(data_all[field])
        return get_date(data_all[field], data_all[FREQUENCY] * i)

    get_start_date = lambda i: _get_date(START, i)
    get_due_date = lambda i: _get_date(DUE, i)

    return [
        WorkType(
            title=f'{prefix} {i + idx}',
            start_date=get_start_date(i),
            due_date=get_due_date(i),
            percent_worth=data_all.get(WORTH) / num,
            course_name=course_name
        )
        for i in range(num)
    ]

def parse_class_work_list(data: list, prefix: str, idx: int, course_name: str, WorkType: Type[ClassWork]) -> Optional[List[ClassWork]]:
    return [
        WorkType(
            title=entry.get(NAME, f'{prefix} {i + idx}'),
            start_date=get_date(entry.get(START)) if START in entry else None,
            due_date=get_date(entry.get(DUE)) if DUE in entry else None,
            percent_worth=entry.get(WORTH),
            course_name=course_name
        )
        for i, entry in enumerate(data)
    ]

def parse_class_work(info: dict, prefix: str, course_name: str, WorkType: Type[ClassWork]) -> Optional[List[ClassWork]]:
    verify_fields([DATA], info)
    idx = info[IDX] if IDX in info else 1
    data = info[DATA]
    if isinstance(data, list):
        return parse_class_work_list(data, prefix, idx, course_name, WorkType)
    else:
        return parse_class_work_group(data, prefix, idx, course_name, WorkType)

def parse_course(course: dict, course_name: str) -> Optional[Course]:
    return Course(
        name=course_name,
        assignments=parse_class_work(course[ASSIGNMENTS], 'Assignment', course_name, Assignment) if ASSIGNMENTS in course else [],
        quizzes=parse_class_work(course[QUIZZES], 'Quiz', course_name, Quiz) if QUIZZES in course else [],
        exams=parse_class_work(course[EXAMS], 'Exam', course_name, Exam) if EXAMS in course else []
    )

def parse_courses_file(file: str) -> Optional[List[Course]]:
    courses_info = load_courses_info(file)[COURSES]
    return [parse_course(courses_info[course_name], course_name) for course_name in courses_info]
