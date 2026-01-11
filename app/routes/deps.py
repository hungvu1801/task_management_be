from sqlmodel import Session
from app.db import engine
from collections.abc import Generator
from typing import Annotated
from fastapi import Depends


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDeps = Annotated[Session, Depends(get_db)]
