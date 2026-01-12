from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, Annotated
import uuid
from app.routes.deps import SessionDeps
from app.schemas import UserCreate, UserRegister, UserPublic, Project, Task
from app.utils import generate_new_account_email, send_email
from app import crud

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/")
def create_user(session: SessionDeps, user_in: UserCreate):
    user = crud.get_user_from_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.create_user(session, user=user_in)
    email_data = generate_new_account_email(
        email_to=user.email, username=user.email, password=user_in.password
    )

    send_email(
        email_to=user_in.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return user


@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDeps, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = crud.get_user_from_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = create_user(session=session, user_create=user_create)
    return user


@router.post("/login")
def login_user(
    session: SessionDeps, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return user


@router.get("/{user_id}/projects", response_model=list[Project])
def get_user_projects(session: SessionDeps, user_id: uuid.UUID):
    user = crud.get_user_from_id(session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.projects


@router.get("/{user_id}/tasks", response_model=list[Task])
def get_user_tasks(session: SessionDeps, user_id: uuid.UUID):
    user = crud.get_user_from_id(session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.tasks
