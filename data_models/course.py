from dataclasses import dataclass
from typing import List

from .assignment import Assignment
from .quiz import Quiz
from .exam import Exam

@dataclass
class Course:
    name: str
    assignments: List[Assignment]
    quizzes: List[Quiz]
    exams: List[Exam]
