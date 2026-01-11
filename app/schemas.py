from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    is_active: bool = True
    is_superuser: bool = False
    name: str


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

    projects: list["Project"] = Relationship(back_populates="owner")
    tasks: list["Task"] = Relationship(back_populates="assignee")


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    owner_id: User | None = Relationship(back_populates="projects")
    task: list["Task"] = Relationship(back_populates="project")


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    status: str = "todo"

    project_id: int = Field(foreign_key="project.id")
    assignee_id: int = Field(foreign_key="user.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: str
    name: str
    password: str
