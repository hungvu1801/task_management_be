from sqlmodel import select

from app.routes.deps import SessionDeps
from app.schemas import User, UserCreate
from app.security import get_password_hash


def get_user_from_email(session: SessionDeps, email: str):
    user = session.exec(select(User).where(User.email == email)).first()
    return user


def create_user(session: SessionDeps, user: UserCreate):
    db_obj = User.model_validate(
        user, update={"hashed_password": get_password_hash(user.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
