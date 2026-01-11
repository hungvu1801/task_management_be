from fastapi import APIRouter
from sqlmodel import select
from app.schemas import Project, ProjectCreate, ProjectRead
from app.routes.deps import SessionDeps


router = APIRouter(prefix="/project", tags=["project"])


@router.post("/", response_model=ProjectRead)
def create_project(
    session: SessionDeps,
    project_in: ProjectCreate,
):
    project = Project(
        project_name=project_in.project_name,
        owner_id=project_in.owner_id,
    )

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


@router.get("/", response_model=list[Project])
def list_projects(session: SessionDeps):
    return session.exec(select(Project)).all()
