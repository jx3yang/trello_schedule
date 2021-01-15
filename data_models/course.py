from dataclasses import dataclass
from typing import List
from textwrap import indent

from .assignment import Assignment
from .quiz import Quiz
from .exam import Exam

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
