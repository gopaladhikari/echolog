from typing import Literal

from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    interval: Literal["monthly", "yearly"]
