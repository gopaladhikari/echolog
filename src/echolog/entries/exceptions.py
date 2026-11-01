from echolog.core.exceptions import APIException, status


class EntryNotFoundException(APIException):
    def __init__(self, entry_id: int) -> None:
        self.entry_id = entry_id
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(f"Entry with id {entry_id} not found")


class SubscriptionLimitExceededException(APIException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        super().__init__(
            "Free tier limit reached. Please upgrade to Pro for unlimited journaling."
        )
