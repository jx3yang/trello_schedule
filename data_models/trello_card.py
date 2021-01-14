from dataclasses import dataclass

@dataclass
class TrelloCard:
    name: str
    desc: str
    start: str # isoformat
    due: str # isoformat
