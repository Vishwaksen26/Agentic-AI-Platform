// Common TypeScript types for enterprise application

export type Status = 'idle' | 'loading' | 'success' | 'error'

export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
  error?: string
  timestamp: string
}

export interface ApiError {
  code: string
  message: string
  details?: Record<string, unknown>
  statusCode: number
  timestamp: string
}

export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'manager' | 'user' | 'viewer'
  avatar?: string
  createdAt: string
}

export interface Workspace {
  id: string
  name: string
  slug: string
  description?: string
  owner: User
  members: User[]
  createdAt: string
  updatedAt: string
}

export interface Agent {
  id: string
  name: string
  description: string
  category: string
  enabled: boolean
  config?: Record<string, unknown>
}

export interface Workflow {
  id: string
  name: string
  description?: string
  nodes: WorkflowNode[]
  edges: WorkflowEdge[]
  status: 'draft' | 'active' | 'archived'
  createdBy: string
  createdAt: string
  updatedAt: string
}

export interface WorkflowNode {
  id: string
  type: string
  data: Record<string, unknown>
  position: { x: number; y: number }
}

export interface WorkflowEdge {
  id: string
  source: string
  target: string
  data?: Record<string, unknown>
}

export interface WorkflowRun {
  id: string
  workflowId: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  startedAt: string
  completedAt?: string
  result?: Record<string, unknown>
  error?: string
}

export interface Approval {
  id: string
  workflowRunId: string
  status: 'pending' | 'approved' | 'rejected'
  requiredBy?: string
  approvedBy?: string
  approvedAt?: string
  comment?: string
}

export interface AuditLog {
  id: string
  userId: string
  action: string
  resource: string
  resourceId: string
  changes?: Record<string, unknown>
  timestamp: string
}

export interface PaginationParams {
  page: number
  limit: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  hasMore: boolean
}
