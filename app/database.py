from sqlalchemy import create_engine
from app.config import DATABASE_URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from typing import Annotated
from fastapi import Depends

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDep = Annotated[Session, Depends(get_db)]