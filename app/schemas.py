from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    name: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

    projects: list["Project"] = Relationship(back_populates="owner")
    tasks: list["Task"] = Relationship(back_populates="assignee")


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    project_name: str
    owner_id: uuid.UUID = Field(foreign_key="user.id")

    owner: User | None = Relationship(back_populates="projects")
    task: list["Task"] = Relationship(back_populates="project")


class ProjectCreate(SQLModel):
    project_name: str
    owner_id: uuid.UUID


class ProjectRead(SQLModel):
    id: int
    project_name: str
    owner_id: uuid.UUID


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    status: str = "todo"

    project_id: int = Field(foreign_key="project.id")
    assignee_id: uuid.UUID = Field(foreign_key="user.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    assignee: User | None = Relationship(back_populates="tasks")
    project: Project | None = Relationship(back_populates="task")


class TaskCreate(SQLModel):
    title: str
    description: str | None = None
    status: str = "todo"
    project_id: int
    assignee_id: uuid.UUID


class TaskRead(SQLModel):
    id: int
    title: str
    description: str
    status: str
    project_id: int
    assignee_id: uuid.UUID


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    name: str = Field(min_length=8, max_length=40)


class UserPublic(UserBase):
    id: uuid.UUID
