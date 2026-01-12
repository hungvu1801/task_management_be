from fastapi import APIRouter

from app.routes import task, project, user, root


api_router = APIRouter()
api_router.include_router(task.router)
api_router.include_router(project.router)
api_router.include_router(user.router)
api_router.include_router(root.router)
