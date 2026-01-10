from fastapi import APIRouter

from app.routers import task, project, user


api_router = APIRouter()
api_router.include_router(task.router)
api_router.include_router(project.router)
api_router.include_router(user.router)
