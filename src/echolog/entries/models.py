from sqlmodel import SQLModel, Field, func
from datetime import datetime


class Entries(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
