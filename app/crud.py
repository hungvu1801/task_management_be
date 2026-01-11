from sqlmodel import select

from app.routes.deps import SessionDeps
from app.schemas import User, UserCreate
from app.security import get_password_hash, verify_password


def get_user_from_email(session: SessionDeps, email: str):
    user = session.exec(select(User).where(User.email == email)).first()
    return user


def create_user(session: SessionDeps, user: UserCreate):
    db_obj = User(
        email=user.email,
        name=user.name,
        hashed_password=get_password_hash(user.password),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def authenticate(session: SessionDeps, email: str, password: str) -> User | None:
    db_user = get_user_from_email(session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
