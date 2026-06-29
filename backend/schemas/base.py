"""Pydantic schemas for request and response validation."""

from datetime import datetime
from typing import Optional, Any, Generic, TypeVar
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, field_validator


# Generic response schema
T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field(default="asc", pattern="^(asc|desc)$")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    data: list[T]
    total: int
    page: int
    limit: int
    has_more: bool


class ErrorResponse(BaseModel):
    """Error response schema."""
    code: str
    message: str
    details: Optional[dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status_code: int


class SuccessResponse(BaseModel, Generic[T]):
    """Generic success response."""
    data: T
    status: int = 200
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# User schemas
class UserRole(str, Enum):
    """User roles."""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    VIEWER = "viewer"


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str = Field(min_length=8)


class UserRegister(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=2, max_length=100)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password complexity."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    email: str
    name: str
    role: UserRole
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# Workflow schemas
class WorkflowNodeData(BaseModel):
    """Workflow node data."""
    id: str
    type: str
    label: str
    position: dict[str, float]
    data: dict[str, Any] = {}


class WorkflowEdgeData(BaseModel):
    """Workflow edge data."""
    id: str
    source: str
    target: str


class WorkflowStatus(str, Enum):
    """Workflow status."""
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class WorkflowCreate(BaseModel):
    """Workflow creation schema."""
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    nodes: list[WorkflowNodeData] = []
    edges: list[WorkflowEdgeData] = []


class WorkflowUpdate(BaseModel):
    """Workflow update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    nodes: Optional[list[WorkflowNodeData]] = None
    edges: Optional[list[WorkflowEdgeData]] = None
    status: Optional[WorkflowStatus] = None


class WorkflowResponse(BaseModel):
    """Workflow response schema."""
    id: str
    name: str
    description: Optional[str]
    status: WorkflowStatus
    nodes: list[WorkflowNodeData]
    edges: list[WorkflowEdgeData]
    created_by: str
    created_at: datetime
    updated_at: datetime


# Approval schemas
class ApprovalStatus(str, Enum):
    """Approval status."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ApprovalDecision(BaseModel):
    """Approval decision schema."""
    status: ApprovalStatus
    comment: Optional[str] = None


class ApprovalResponse(BaseModel):
    """Approval response schema."""
    id: str
    workflow_run_id: str
    status: ApprovalStatus
    required_by: Optional[str]
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    comment: Optional[str]
    created_at: datetime


# Analytics schemas
class AnalyticMetric(BaseModel):
    """Analytics metric."""
    name: str
    value: Any
    unit: Optional[str] = None
    trend: Optional[str] = None


class AnalyticsResponse(BaseModel):
    """Analytics response schema."""
    total_workflows: int
    active_runs: int
    completed_runs: int
    failed_runs: int
    total_tokens_used: int
    success_rate: float
    avg_execution_time: float
    metrics: list[AnalyticMetric]
    timestamp: datetime
