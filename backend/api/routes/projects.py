from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.connection import get_db
from backend.database.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from backend.services.workspace_service import create_project, delete_project, get_project, list_projects, update_project

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=list[ProjectResponse])
async def get_projects(session: AsyncSession = Depends(get_db)):
    return await list_projects(session)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_by_id(project_id: str, session: AsyncSession = Depends(get_db)):
    try:
        return await get_project(session, project_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Project not found: {exc.args[0]}") from exc


@router.post("", response_model=ProjectResponse)
async def create_project_route(payload: ProjectCreate, session: AsyncSession = Depends(get_db)):
    return await create_project(session, payload)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project_route(project_id: str, payload: ProjectUpdate, session: AsyncSession = Depends(get_db)):
    try:
        return await update_project(session, project_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Project not found: {exc.args[0]}") from exc


@router.delete("/{project_id}")
async def delete_project_route(project_id: str, session: AsyncSession = Depends(get_db)):
    try:
        await delete_project(session, project_id)
        return {"deleted": True, "project_id": project_id}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Project not found: {exc.args[0]}") from exc