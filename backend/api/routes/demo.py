from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.demo_runtime import runtime
from backend.database.connection import get_db
from backend.database.schemas import RunWorkflowRequest
from backend.services.workspace_service import list_projects, list_workflows

router = APIRouter(prefix="/demo", tags=["Demo"])


@router.get("/bootstrap")
async def demo_bootstrap(session: AsyncSession = Depends(get_db)):
    snapshot = runtime.get_dashboard_snapshot()
    snapshot["projects"] = await list_projects(session)
    snapshot["workflows"] = await list_workflows(session)
    return snapshot


@router.post("/start")
async def demo_start(request: RunWorkflowRequest):
    try:
        return await runtime.launch_demo_run(workflow_id=request.workflow_id, input_data=request.input_data)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {exc.args[0]}") from exc