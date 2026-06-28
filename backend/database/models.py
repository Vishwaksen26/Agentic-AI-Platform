"""AgentForge AI Backend – Database Models (SQLAlchemy 2.0 async)"""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def gen_uuid() -> str:
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    role: Mapped[str] = mapped_column(String(50), default="user")  # admin|user|viewer
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    workflows: Mapped[list["Workflow"]] = relationship("Workflow", back_populates="owner")
    projects: Mapped[list["Project"]] = relationship("Project", back_populates="owner")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str] = mapped_column(String(7), default="#6366f1")
    icon: Mapped[str] = mapped_column(String(50), default="folder")
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="projects")
    workflows: Mapped[list["Workflow"]] = relationship("Workflow", back_populates="project")


class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(50), default="draft")  # draft|active|archived
    graph_data: Mapped[dict] = mapped_column(JSON, default=dict)  # React Flow nodes/edges
    agent_config: Mapped[dict] = mapped_column(JSON, default=dict)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    project_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("projects.id"), nullable=True)
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="workflows")
    project: Mapped["Project | None"] = relationship("Project", back_populates="workflows")
    runs: Mapped[list["WorkflowRun"]] = relationship("WorkflowRun", back_populates="workflow")


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("workflows.id"))
    status: Mapped[str] = mapped_column(String(50), default="queued")  # queued|running|paused|completed|failed
    trigger: Mapped[str] = mapped_column(String(50), default="manual")  # manual|scheduled|api|demo
    input_data: Mapped[dict] = mapped_column(JSON, default=dict)
    output_data: Mapped[dict] = mapped_column(JSON, default=dict)
    planner_reasoning: Mapped[list] = mapped_column(JSON, default=list)
    agent_results: Mapped[dict] = mapped_column(JSON, default=dict)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    workflow: Mapped["Workflow"] = relationship("Workflow", back_populates="runs")
    agent_logs: Mapped[list["AgentLog"]] = relationship("AgentLog", back_populates="run")
    approvals: Mapped[list["HumanApproval"]] = relationship("HumanApproval", back_populates="run")
    companies: Mapped[list["DiscoveredCompany"]] = relationship("DiscoveredCompany", back_populates="run")


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("workflow_runs.id"))
    agent_id: Mapped[str] = mapped_column(String(100))
    agent_name: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50))  # started|running|completed|failed|skipped
    input_data: Mapped[dict] = mapped_column(JSON, default=dict)
    output_data: Mapped[dict] = mapped_column(JSON, default=dict)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    token_usage: Mapped[int] = mapped_column(Integer, default=0)
    elapsed_ms: Mapped[int] = mapped_column(Integer, default=0)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    run: Mapped["WorkflowRun"] = relationship("WorkflowRun", back_populates="agent_logs")


class HumanApproval(Base):
    __tablename__ = "human_approvals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("workflow_runs.id"))
    agent_id: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending|approved|rejected|edited
    reviewer_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    edited_content: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    reviewed_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    run: Mapped["WorkflowRun"] = relationship("WorkflowRun", back_populates="approvals")


class DiscoveredCompany(Base):
    __tablename__ = "discovered_companies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("workflow_runs.id"))
    name: Mapped[str] = mapped_column(String(255))
    domain: Mapped[str] = mapped_column(String(255))
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    employee_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    revenue_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    icp_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    tech_stack: Mapped[list] = mapped_column(JSON, default=list)
    decision_makers: Mapped[list] = mapped_column(JSON, default=list)
    enrichment_data: Mapped[dict] = mapped_column(JSON, default=dict)
    recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    recommended_action: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    run: Mapped["WorkflowRun"] = relationship("WorkflowRun", back_populates="companies")


class MemoryEntry(Base):
    __tablename__ = "memory_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    key: Mapped[str] = mapped_column(String(500), index=True)
    value: Mapped[dict] = mapped_column(JSON)
    memory_type: Mapped[str] = mapped_column(String(50))  # company|contact|search|planner|workflow|user_pref
    source_run_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    ttl_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    access_count: Mapped[int] = mapped_column(Integer, default=0)
    last_accessed: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=gen_uuid)
    actor_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    resource_type: Mapped[str] = mapped_column(String(50))
    resource_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    event_metadata: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
