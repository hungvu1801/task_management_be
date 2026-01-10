import uvicorn
from pathlib import Path


from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.routers import api_router
# from starlette.middleware.cors import CORSMiddleware

# from app.api.main import api_router
from app.core.config import settings



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # set up project root directory
    project_root = Path(__file__).parent.parent.resolve()
    print(project_root)

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)