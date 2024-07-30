from typing import Annotated
from sqlmodel import Session
from fastapi import Depends
from databases.database import engine


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close


SessionDepend = Annotated[Session, Depends(get_db)]
