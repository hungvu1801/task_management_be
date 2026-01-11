from sqlmodel import Session
from app.schemas import User, Project, Task
from app.db import engine


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models

    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    with Session(engine) as session:
        init_db(session)
    session.commit()
