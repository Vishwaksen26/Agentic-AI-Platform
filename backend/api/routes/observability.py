from fastapi import APIRouter

from backend.core.demo_runtime import runtime

router = APIRouter(tags=["Observability"])


@router.get("/agents")
async def list_agents():
    return runtime.list_agents()


@router.get("/dashboard")
async def dashboard_snapshot():
    return runtime.get_dashboard_snapshot()


@router.get("/analytics/summary")
async def analytics_summary():
    return runtime.get_analytics_summary()


@router.get("/memory")
async def memory_entries():
    return runtime.get_memory_entries()


@router.get("/reports")
async def reports():
    return runtime.get_reports()


@router.get("/notifications")
async def notifications():
    return runtime.get_notifications()


@router.get("/planner/activity")
async def planner_activity():
    return runtime.get_planner_activity()