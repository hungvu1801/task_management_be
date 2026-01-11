from fastapi import APIRouter, HTTPException

from app.routes.deps import SessionDeps
from app.schemas import UserCreate
from app.crud import get_user_from_email, create_user
from app.utils import generate_new_account_email

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/")
def create_user(session: SessionDeps, user_in: UserCreate):
    user = get_user_from_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = create_user(session, user=user_in)
    email_data = generate_new_account_email(
        email_to=user.email, password=user_in.password
    )
