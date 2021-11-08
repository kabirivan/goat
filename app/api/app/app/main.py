from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app import crud
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import async_session

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup_event():
    print("App is starting...")
    async with async_session() as db:
        table_index = await crud.layer.table_index(db)
        app.state.Catalog = table_index


app.include_router(api_router, prefix=settings.API_V1_STR)