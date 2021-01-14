from dataclasses import dataclass

@dataclass
class TrelloBoard:
    board_id: str
    name: str
    start_date_id: str
