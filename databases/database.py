from sqlmodel import create_engine, SQLModel
from config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(engine)
