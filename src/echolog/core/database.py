from sqlmodel import Session, SQLModel, create_engine

from .config import config

engine = create_engine(config.database_url, echo=True)


def create_table():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
