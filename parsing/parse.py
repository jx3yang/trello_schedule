from .utils import load_board_info, load_courses_info, not_found_fields, verify_fields
from .constants import *

from data_models import *
from trello_api import get_board_id, get_list_id, get_custom_field_id
from time_utils import *

import datetime as dt
from typing import List, Optional, Tuple, Type

Credentials = TrelloCredentials

def parse_board_file(credentials: Credentials, file: str) -> Optional[Tuple[TrelloBoard, TrelloList]]:
    board_info = load_board_info(file)
    board_name = board_info[BOARD]
    list_name = board_info[LIST]
    start_date_field = board_info[START_DATE_FIELD]
    board_id = get_board_id(credentials, board_name)
    list_id = get_list_id(credentials, board_id, list_name)
    start_date_id = get_custom_field_id(credentials, board_id, start_date_field)

    trello_board = TrelloBoard(board_id=board_id, name=board_name, start_date_id=start_date_id)
    trello_list = TrelloList(list_id=list_id, name=list_name)
    return trello_board, trello_list

def _parse_agg_entry(data_agg: dict, prefix: str, idx: int, WorkType: Type[ClassWork]) -> Optional[List[ClassWork]]:
    verify_fields([NUM], data_agg)
    num = data_agg[NUM]
    excepts = [
        { START: get_date_dt(entry[START]), DUE: get_date_dt(entry[DUE]) } for entry in sorted(data_agg[EXCEPT], key=lambda x: get_date(x[START]))
    ] if EXCEPT in data_agg else []

    def correction_factor(dt_obj: dt.datetime, excepts: List[dict]) -> int:
        factor = 0
        for e in excepts:
            if e[START] <= dt_obj <= e[DUE] or e[DUE] < dt_obj:
                factor += 1
            else:
                return factor
        return factor
    
    def _get_date(field: str, i: int):
        has_not_found, not_found = not_found_fields([field, FREQUENCY], data_agg)
        if has_not_found:
            if field in not_found: return None
            if FREQUENCY in not_found: return get_date(data_agg[field])
        date = get_date_dt(data_agg[field], data_agg[FREQUENCY] * i)
        correction = correction_factor(date, excepts)
        if correction > 0: return get_date(data_agg[field], data_agg[FREQUENCY] * (i + correction))
        return date.isoformat()
    
    get_start_date = lambda i: _get_date(START, i)
    get_due_date = lambda i: _get_date(DUE, i)

    idx = data_agg[IDX] if IDX in data_agg else idx
    return [
        WorkType(
            title=f'{prefix} {i + idx}',
            start_date=get_start_date(i),
            due_date=get_due_date(i),
            percent_worth=data_agg.get(WORTH) / num
        )
        for i in range(num)
    ]

def _parse_entry(data_entry: dict, prefix: str, idx: int, WorkType: Type[ClassWork]) -> ClassWork:
    return WorkType(
        title=data_entry.get(NAME, f'{prefix} {idx}'),
        start_date=get_date(data_entry.get(START)) if START in data_entry else None,
        due_date=get_date(data_entry.get(DUE)) if DUE in data_entry else None,
        percent_worth=data_entry.get(WORTH)
    )

def parse_class_work_agg(data: dict, prefix: str, idx: int, WorkType: Type[ClassWork]) -> Optional[List[ClassWork]]:
    data_agg = data[AGG]
    return _parse_agg_entry(data_agg, prefix, idx, WorkType)

def parse_class_work_group(data: dict, prefix: str, idx: int, WorkType: Type[ClassWork]) -> Optional[List[ClassWork]]:
    data_group = data[GROUP]
    results = []
    for group in data_group:
        if AGG in group:
            results.extend(_parse_agg_entry(group[AGG], prefix, idx + len(results), WorkType))
        else:
            results.append(_parse_entry(group, prefix, idx + len(results), WorkType))
    return results

def parse_class_work_list(data: list, prefix: str, idx: int, WorkType: Type[ClassWork]) -> Optional[List[ClassWork]]:
    return [_parse_entry(entry, prefix, i + idx, WorkType) for i, entry in enumerate(data)]
            # WorkType(
        #     title=entry.get(NAME, f'{prefix} {i + idx}'),
        #     start_date=get_date(entry.get(START)) if START in entry else None,
        #     due_date=get_date(entry.get(DUE)) if DUE in entry else None,
        #     percent_worth=entry.get(WORTH)
        # )

def parse_class_work(info: dict, prefix: str, WorkType: Type[ClassWork]) -> Optional[List[ClassWork]]:
    verify_fields([DATA], info)
    idx = info[IDX] if IDX in info else 1
    data = info[DATA]
    if isinstance(data, list):
        return parse_class_work_list(data, prefix, idx, WorkType)
    elif AGG in data:
        return parse_class_work_agg(data, prefix, idx, WorkType)
    elif GROUP in data:
        return parse_class_work_group(data, prefix, idx, WorkType)
    return None

def parse_course(course: dict, course_name: str) -> Optional[Course]:
    return Course(
        name=course_name,
        assignments=parse_class_work(course[ASSIGNMENTS], 'Assignment', Assignment) if ASSIGNMENTS in course else [],
        quizzes=parse_class_work(course[QUIZZES], 'Quiz', Quiz) if QUIZZES in course else [],
        exams=parse_class_work(course[EXAMS], 'Exam', Exam) if EXAMS in course else []
    )

def parse_courses_file(file: str) -> Optional[List[Course]]:
    courses_info = load_courses_info(file)[COURSES]
    return [parse_course(courses_info[course_name], course_name) for course_name in courses_info]
