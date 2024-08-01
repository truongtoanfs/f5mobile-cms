from sqlmodel import create_engine, SQLModel

SQLALCHEMY_DATABASE_URL = "mysql://root:tf_pypM3322@45.124.95.107:3306/f5mobile"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(engine)
