from fastapi import APIRouter

from app.api.api_v1.endpoints import (  # vectortiles,
    isochrones,
    items,
    login,
    scenarios,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(isochrones.router, prefix="/isochrones", tags=["isochrones"])
api_router.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
# api_router.include_router(vectortiles.router, prefix="/vectortiles", tags=["vectortiles"])