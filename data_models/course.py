from dataclasses import dataclass
from textwrap import indent
from typing import List

from .assignment import Assignment
from .exam import Exam
from .quiz import Quiz


@dataclass
class Course:
    name: str
    assignments: List[Assignment]
    quizzes: List[Quiz]
    exams: List[Exam]

    def __str__(self):
        works_strings = lambda works: indent('\n'.join(str(work) for work in works), '')
        return f'''\
Course: {self.name}

Assignments:
{works_strings(self.assignments)}

Quizzes:
{works_strings(self.quizzes)}

Exams:
{works_strings(self.exams)}
'''
