from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import Any
from app.schemas import Task
from app.routes.deps import SessionDeps

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", response_model=Task)
def create_task(task: Task, session: SessionDeps):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/", response_model=list[Task])
def list_tasks(session: SessionDeps):
    return session.exec(select(Task)).all()
