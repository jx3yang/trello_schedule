from dataclasses import dataclass
import datetime as dt

@dataclass
class ClassWork:
    title: str
    start_date: dt.datetime
    end_date: dt.datetime
    percent_worth: float
    course_name: str
