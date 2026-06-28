"""AgentForge AI – Pydantic Schemas (API request/response models)"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field


# ─── Common ───────────────────────────────────────────────────────────────────

class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int
    page: int
    page_size: int
    has_next: bool


# ─── Auth ─────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: str
    name: str
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    avatar_url: Optional[str] = None
    role: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LoginRequest(BaseModel):
    email: str
    password: str


# ─── Projects ─────────────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    color: str = "#6366f1"
    icon: str = "folder"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    color: str
    icon: str
    owner_id: str
    created_at: datetime
    workflow_count: int = 0

    model_config = {"from_attributes": True}


# ─── Workflows ────────────────────────────────────────────────────────────────

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: Optional[str] = None
    graph_data: dict = Field(default_factory=dict)
    agent_config: dict = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    graph_data: Optional[dict] = None
    agent_config: Optional[dict] = None
    tags: Optional[list[str]] = None
    status: Optional[str] = None


class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    version: int
    status: str
    graph_data: dict
    agent_config: dict
    tags: list[str]
    project_id: Optional[str]
    owner_id: str
    created_at: datetime
    updated_at: datetime
    run_count: int = 0
    last_run_status: Optional[str] = None

    model_config = {"from_attributes": True}


# ─── Workflow Runs ────────────────────────────────────────────────────────────

class RunWorkflowRequest(BaseModel):
    workflow_id: str
    input_data: dict = Field(default_factory=dict)
    demo_mode: bool = False


class WorkflowRunResponse(BaseModel):
    id: str
    workflow_id: str
    status: str
    trigger: str
    input_data: dict
    output_data: dict
    planner_reasoning: list
    agent_results: dict
    total_tokens: int
    total_cost_usd: float
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Agents ───────────────────────────────────────────────────────────────────

class AgentInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    capabilities: list[str]
    avg_token_usage: int
    avg_execution_ms: int
    success_rate: float
    icon: str
    color: str


# ─── Memory ───────────────────────────────────────────────────────────────────

class MemoryEntryResponse(BaseModel):
    id: str
    key: str
    value: dict
    memory_type: str
    source_run_id: Optional[str]
    access_count: int
    last_accessed: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Approvals ────────────────────────────────────────────────────────────────

class ApprovalResponse(BaseModel):
    id: str
    run_id: str
    agent_id: str
    title: str
    content: dict
    status: str
    reviewer_comment: Optional[str]
    edited_content: Optional[dict]
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}


class ApprovalDecision(BaseModel):
    decision: str  # approved|rejected|edited
    comment: Optional[str] = None
    edited_content: Optional[dict] = None


# ─── Analytics ────────────────────────────────────────────────────────────────

class AnalyticsSummary(BaseModel):
    total_workflows: int
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float
    total_tokens_used: int
    total_cost_usd: float
    avg_execution_time_ms: int
    active_agents_count: int
    memory_hit_rate: float
    pending_approvals: int
    companies_discovered: int


class TimeSeriesPoint(BaseModel):
    timestamp: datetime
    value: float


class AgentUsageStat(BaseModel):
    agent_id: str
    agent_name: str
    total_executions: int
    success_rate: float
    avg_token_usage: int
    avg_execution_ms: int


# ─── Reports ─────────────────────────────────────────────────────────────────

class ReportResponse(BaseModel):
    id: str
    run_id: str
    title: str
    format: str
    file_path: Optional[str]
    shareable_url: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Notifications ────────────────────────────────────────────────────────────

class NotificationResponse(BaseModel):
    id: str
    type: str  # workflow_completed|agent_failed|approval_required|report_ready|retry_completed
    title: str
    message: str
    read: bool
    metadata: dict
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Company Discovery ────────────────────────────────────────────────────────

class DecisionMaker(BaseModel):
    name: str
    title: str
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    confidence: float = 0.0


class CompanyResponse(BaseModel):
    id: str
    run_id: str
    name: str
    domain: str
    industry: Optional[str]
    employee_count: Optional[int]
    revenue_usd: Optional[float]
    location: Optional[str]
    icp_score: float
    confidence: float
    tech_stack: list[str]
    decision_makers: list[dict]
    enrichment_data: dict
    recommendation: Optional[str]
    recommended_action: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
