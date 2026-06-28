"""Database-backed workspace CRUD and demo seeding helpers."""

from __future__ import annotations

from typing import Any

from sqlalchemy import Select, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.agents.registry import build_default_workflow_graph
from backend.database.models import Project, User, Workflow, WorkflowRun
from backend.database.schemas import ProjectCreate, ProjectUpdate, WorkflowCreate, WorkflowUpdate

DEMO_USER_EMAIL = "demo@agentforge.local"
DEMO_USER_NAME = "Demo User"
DEMO_PROJECT_NAME = "Prospect Intelligence"
DEMO_WORKFLOW_NAME = "Customer Discovery Orchestration"


def _workflow_payload(workflow: Workflow, run_count: int = 0, last_run_status: str | None = None) -> dict[str, Any]:
    return {
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "version": workflow.version,
        "status": workflow.status,
        "graph_data": workflow.graph_data,
        "agent_config": workflow.agent_config,
        "tags": list(workflow.tags or []),
        "project_id": workflow.project_id,
        "owner_id": workflow.owner_id,
        "created_at": workflow.created_at,
        "updated_at": workflow.updated_at,
        "run_count": run_count,
        "last_run_status": last_run_status,
    }


def _project_payload(project: Project, workflow_count: int = 0) -> dict[str, Any]:
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "color": project.color,
        "icon": project.icon,
        "owner_id": project.owner_id,
        "created_at": project.created_at,
        "workflow_count": workflow_count,
    }


async def ensure_demo_workspace(session: AsyncSession) -> None:
    user_result = await session.execute(select(User).where(User.email == DEMO_USER_EMAIL))
    user = user_result.scalar_one_or_none()
    if user is None:
        user = User(email=DEMO_USER_EMAIL, name=DEMO_USER_NAME, role="admin")
        session.add(user)
        await session.flush()

    project_result = await session.execute(select(Project).where(Project.name == DEMO_PROJECT_NAME, Project.owner_id == user.id))
    project = project_result.scalar_one_or_none()
    if project is None:
        project = Project(
            name=DEMO_PROJECT_NAME,
            description="B2B customer discovery workspace for demo and production workflows.",
            color="#6366f1",
            icon="sparkles",
            owner_id=user.id,
        )
        session.add(project)
        await session.flush()

    workflow_result = await session.execute(select(Workflow).where(Workflow.name == DEMO_WORKFLOW_NAME, Workflow.owner_id == user.id))
    workflow = workflow_result.scalar_one_or_none()
    if workflow is None:
        workflow = Workflow(
            name=DEMO_WORKFLOW_NAME,
            description="Monitor market signals, validate companies, enrich contacts, and route to review.",
            version=4,
            status="active",
            graph_data=build_default_workflow_graph(),
            agent_config={"planner": {"enabled": True}},
            tags=["demo", "b2b", "prospect-intelligence"],
            project_id=project.id,
            owner_id=user.id,
        )
        session.add(workflow)


async def list_projects(session: AsyncSession) -> list[dict[str, Any]]:
    workflow_counts = select(
        Workflow.project_id.label("project_id"),
        func.count(Workflow.id).label("workflow_count"),
    ).group_by(Workflow.project_id).subquery()

    statement: Select[Any] = (
        select(Project, func.coalesce(workflow_counts.c.workflow_count, 0))
        .outerjoin(workflow_counts, workflow_counts.c.project_id == Project.id)
        .order_by(Project.created_at.desc())
    )
    result = await session.execute(statement)
    projects: list[dict[str, Any]] = []
    for project, workflow_count in result.all():
        projects.append(_project_payload(project, int(workflow_count or 0)))
    return projects


async def get_project(session: AsyncSession, project_id: str) -> dict[str, Any]:
    project = await session.get(Project, project_id)
    if project is None:
        raise KeyError(project_id)
    workflow_count = await session.scalar(select(func.count(Workflow.id)).where(Workflow.project_id == project_id))
    return _project_payload(project, int(workflow_count or 0))


async def create_project(session: AsyncSession, payload: ProjectCreate) -> dict[str, Any]:
    user_result = await session.execute(select(User).where(User.email == DEMO_USER_EMAIL))
    user = user_result.scalar_one_or_none()
    if user is None:
        user = User(email=DEMO_USER_EMAIL, name=DEMO_USER_NAME, role="admin")
        session.add(user)
        await session.flush()

    project = Project(
        name=payload.name,
        description=payload.description,
        color=payload.color,
        icon=payload.icon,
        owner_id=user.id,
    )
    session.add(project)
    await session.flush()
    return _project_payload(project, 0)


async def update_project(session: AsyncSession, project_id: str, payload: ProjectUpdate) -> dict[str, Any]:
    project = await session.get(Project, project_id)
    if project is None:
        raise KeyError(project_id)

    for field in ("name", "description", "color", "icon"):
        value = getattr(payload, field)
        if value is not None:
            setattr(project, field, value)

    await session.flush()
    workflow_count = await session.scalar(select(func.count(Workflow.id)).where(Workflow.project_id == project_id))
    return _project_payload(project, int(workflow_count or 0))


async def delete_project(session: AsyncSession, project_id: str) -> None:
    project = await session.get(Project, project_id)
    if project is None:
        raise KeyError(project_id)
    await session.delete(project)


async def list_workflows(session: AsyncSession) -> list[dict[str, Any]]:
    result = await session.execute(select(Workflow).order_by(Workflow.updated_at.desc()))
    workflows: list[dict[str, Any]] = []
    for workflow in result.scalars().all():
        run_count = await session.scalar(select(func.count(WorkflowRun.id)).where(WorkflowRun.workflow_id == workflow.id))
        last_run_status = await session.scalar(
            select(WorkflowRun.status)
            .where(WorkflowRun.workflow_id == workflow.id)
            .order_by(desc(WorkflowRun.created_at))
            .limit(1)
        )
        workflows.append(_workflow_payload(workflow, int(run_count or 0), last_run_status))
    return workflows


async def get_workflow(session: AsyncSession, workflow_id: str) -> dict[str, Any]:
    workflow = await session.get(Workflow, workflow_id)
    if workflow is None:
        raise KeyError(workflow_id)
    run_count = await session.scalar(select(func.count(WorkflowRun.id)).where(WorkflowRun.workflow_id == workflow_id))
    latest_run = await session.scalar(select(WorkflowRun.status).where(WorkflowRun.workflow_id == workflow_id).order_by(desc(WorkflowRun.created_at)).limit(1))
    return _workflow_payload(workflow, int(run_count or 0), latest_run)


async def create_workflow(session: AsyncSession, payload: WorkflowCreate) -> dict[str, Any]:
    user_result = await session.execute(select(User).where(User.email == DEMO_USER_EMAIL))
    user = user_result.scalar_one_or_none()
    if user is None:
        user = User(email=DEMO_USER_EMAIL, name=DEMO_USER_NAME, role="admin")
        session.add(user)
        await session.flush()

    workflow = Workflow(
        name=payload.name,
        description=payload.description,
        version=1,
        status="draft",
        graph_data=payload.graph_data or build_default_workflow_graph(),
        agent_config=payload.agent_config or {},
        tags=payload.tags,
        project_id=payload.project_id,
        owner_id=user.id,
    )
    session.add(workflow)
    await session.flush()
    return _workflow_payload(workflow, 0, None)


async def update_workflow(session: AsyncSession, workflow_id: str, payload: WorkflowUpdate) -> dict[str, Any]:
    workflow = await session.get(Workflow, workflow_id)
    if workflow is None:
        raise KeyError(workflow_id)

    for field in ("name", "description", "graph_data", "agent_config", "tags", "status"):
        value = getattr(payload, field)
        if value is not None:
            setattr(workflow, field, value)
    workflow.version += 1
    await session.flush()
    run_count = await session.scalar(select(func.count(WorkflowRun.id)).where(WorkflowRun.workflow_id == workflow_id))
    latest_run = await session.scalar(select(WorkflowRun.status).where(WorkflowRun.workflow_id == workflow_id).order_by(desc(WorkflowRun.created_at)).limit(1))
    return _workflow_payload(workflow, int(run_count or 0), latest_run)


async def duplicate_workflow(session: AsyncSession, workflow_id: str) -> dict[str, Any]:
    source = await session.get(Workflow, workflow_id)
    if source is None:
        raise KeyError(workflow_id)

    duplicate = Workflow(
        name=f"{source.name} Copy",
        description=source.description,
        version=1,
        status="draft",
        graph_data=source.graph_data,
        agent_config=source.agent_config,
        tags=list(source.tags or []),
        project_id=source.project_id,
        owner_id=source.owner_id,
    )
    session.add(duplicate)
    await session.flush()
    return _workflow_payload(duplicate, 0, None)


async def delete_workflow(session: AsyncSession, workflow_id: str) -> None:
    workflow = await session.get(Workflow, workflow_id)
    if workflow is None:
        raise KeyError(workflow_id)
    await session.delete(workflow)