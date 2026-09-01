from echolog.core.exceptions import APIException


class EntryNotFoundException(APIException):
    def __init__(self, entry_id: int) -> None:
        self.entry_id = entry_id
        super().__init__(f"Entry with id {entry_id} not found")
