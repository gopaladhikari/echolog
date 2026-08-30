from fastapi import Request
from fastapi.responses import JSONResponse


class EntryNotFoundException(Exception):
    def __init__(self, entry_id: int) -> None:
        self.entry_id = entry_id
