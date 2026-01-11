from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from typing import Any
from app.schemas import Task, TaskRead, TaskCreate
from app.routes.deps import SessionDeps

router = APIRouter(prefix="/task", tags=["task"])


@router.post("/", response_model=TaskRead)
def create_task(task_in: TaskCreate, session: SessionDeps):
    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        project_id=task_in.project_id,
        assignee_id=task_in.assignee_id,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/", response_model=list[Task])
def list_tasks(session: SessionDeps):
    return session.exec(select(Task)).all()
