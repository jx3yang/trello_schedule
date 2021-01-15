from dataclasses import dataclass

@dataclass
class ClassWork:
    title: str
    start_date: str
    due_date: str
    percent_worth: float

    def __str__(self):
        return f'''\
Title: {self.title}
    Start Date: {self.start_date}
    Due Date: {self.due_date}
    Worth: {self.percent_worth}%
'''
