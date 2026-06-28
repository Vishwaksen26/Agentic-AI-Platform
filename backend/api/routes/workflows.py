from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.demo_runtime import runtime
from backend.database.connection import get_db
from backend.database.schemas import RunWorkflowRequest, WorkflowCreate, WorkflowUpdate
from backend.services.workspace_service import (
    create_workflow as db_create_workflow,
    delete_workflow as db_delete_workflow,
    duplicate_workflow as db_duplicate_workflow,
    get_workflow as db_get_workflow,
    list_workflows as db_list_workflows,
    update_workflow as db_update_workflow,
)

router = APIRouter(prefix="/workflows", tags=["Workflows"])


@router.get("")
async def list_workflows(session: AsyncSession = Depends(get_db)):
    return await db_list_workflows(session)


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str, session: AsyncSession = Depends(get_db)):
    try:
        return await db_get_workflow(session, workflow_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {exc.args[0]}") from exc


@router.post("")
async def create_workflow(request: WorkflowCreate, session: AsyncSession = Depends(get_db)):
    return await db_create_workflow(session, request)


@router.patch("/{workflow_id}")
async def update_workflow(workflow_id: str, request: WorkflowUpdate, session: AsyncSession = Depends(get_db)):
    try:
        return await db_update_workflow(session, workflow_id, request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {exc.args[0]}") from exc


@router.post("/{workflow_id}/duplicate")
async def duplicate_workflow(workflow_id: str, session: AsyncSession = Depends(get_db)):
    try:
        return await db_duplicate_workflow(session, workflow_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {exc.args[0]}") from exc


@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str, session: AsyncSession = Depends(get_db)):
    try:
        await db_delete_workflow(session, workflow_id)
        return {"deleted": True, "workflow_id": workflow_id}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {exc.args[0]}") from exc


@router.post("/{workflow_id}/run")
async def run_workflow(workflow_id: str, request: RunWorkflowRequest | None = None):
    try:
        return await runtime.launch_demo_run(workflow_id=workflow_id, input_data=request.input_data if request else None)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {exc.args[0]}") from exc


@router.get("/runs/{run_id}")
async def get_run(run_id: str):
    try:
        return runtime.get_run(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Run not found: {exc.args[0]}") from exc