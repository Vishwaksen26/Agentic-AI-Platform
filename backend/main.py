from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.approvals import router as approvals_router
from backend.api.routes.demo import router as demo_router
from backend.api.routes.health import router as health_router
from backend.api.routes.observability import router as observability_router
from backend.api.routes.websocket import router as websocket_router
from backend.api.routes.workflows import router as workflows_router
from backend.core.config import settings
from backend.database.connection import close_db, init_db
from backend.services.workspace_service import ensure_demo_workspace


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async for session in init_db.session_factory():
        await ensure_demo_workspace(session)
        await session.commit()
        break
    yield
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(demo_router, prefix=settings.api_prefix)
app.include_router(__import__("backend.api.routes.projects", fromlist=["router"]).router, prefix=settings.api_prefix)
app.include_router(workflows_router, prefix=settings.api_prefix)
app.include_router(approvals_router, prefix=settings.api_prefix)
app.include_router(observability_router, prefix=settings.api_prefix)
app.include_router(websocket_router)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "api_prefix": settings.api_prefix,
        "demo_mode": settings.demo_mode,
    }