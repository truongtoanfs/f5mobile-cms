from sqlmodel import create_engine, SQLModel

SQLALCHEMY_DATABASE_URL = "mysql://user:password@127.0.0.1:3306/f5mobile"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(engine)
