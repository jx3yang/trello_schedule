from typing import List
import yaml
from .constants import BOARD, COURSES, LIST

def raise_fields_not_found(fields: List[str]):
    quotes = lambda x: f'"{x}"'
    fields_strings = ', '.join(quotes(field) for field in fields)
    raise Exception(f'Requires {fields_strings} field(s)')

def not_found_fields(fields: List[str], obj: dict):
    not_found = [field for field in fields if field not in obj]
    if len(not_found) > 0: return True, not_found
    return False, not_found

def verify_fields(fields: List[str], obj: dict):
    has_not_found, not_found = not_found_fields(fields, obj)
    if has_not_found: raise_fields_not_found(not_found)

def load_from_file(file: str, fields: List[str]):
    with open(file, 'r') as f:
        data = yaml.safe_load(f)
    verify_fields(fields, data)
    return data

def load_courses_info(file: str):
    return load_from_file(file, [COURSES])

def load_board_info(file: str):
    return load_from_file(file, [BOARD, LIST])
