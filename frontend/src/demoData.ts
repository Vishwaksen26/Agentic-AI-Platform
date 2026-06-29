export type CompanyCard = {
  id: string
  name: string
  domain: string
  industry: string
  employee_count: number
  revenue_usd: number
  location: string
  icp_score: number
  confidence: number
  logo_color: string
  tech_stack: string[]
  decision_makers: Array<{ name: string; title: string; email?: string; phone?: string; linkedin_url?: string }>
  recommendation: string
  recommended_action: string
  news_snippet: string
  growth_signals: string[]
}

export type WorkflowGraph = {
  nodes: Array<{
    id: string
    type?: string
    position: { x: number; y: number }
    data: { label: string; description: string; category: string; icon: string; color: string }
    style?: Record<string, string | number>
  }>
  edges: Array<{ id: string; source: string; target: string; animated?: boolean; style?: Record<string, string | number> }>
  viewport: { x: number; y: number; zoom: number }
}

export type BootstrapData = {
  metrics: {
    total_workflows: number
    total_runs: number
    successful_runs: number
    failed_runs: number
    success_rate: number
    total_tokens_used: number
    total_cost_usd: number
    avg_execution_time_ms: number
    active_agents_count: number
    memory_hit_rate: number
    pending_approvals: number
    companies_discovered: number
  }
  workflow_status: { live_runs: number; paused_runs: number; completed_today: number; pending_approvals: number }
  planner: { stage: string; message: string; reasoning: string[] }
  projects: Array<{ id: string; name: string; description: string; color: string; icon: string; workflow_count: number }>
  workflows: Array<{ id: string; name: string; description: string; status: string; version: number; graph_data: WorkflowGraph }>
  running_jobs: Array<{ id: string; name: string; status: string; progress: number; current_step: string; planner_message: string; total_tokens: number }>
  recent_runs: Array<{ id: string; name: string; status: string; progress: number; current_step: string; planner_message: string; total_tokens: number }>
  agents: Array<{ id: string; name: string; description: string; category: string; capabilities: string[]; icon: string; color: string; success_rate: number; avg_token_usage: number; avg_execution_ms: number }>
  companies: CompanyCard[]
  approvals: Array<{ id: string; run_id: string; agent_id: string; title: string; content: { headline: string; summary: string; companies: CompanyCard[] }; status: string }>
  reports: Array<{ id: string; run_id?: string | null; title: string; format: string; shareable_url?: string | null; created_at: string }>
  notifications: Array<{ id: string; type: string; title: string; message: string; read: boolean; created_at: string }>
  memory: { total_entries: number; groups: Record<string, Array<{ id: string; key: string; value: Record<string, unknown>; memory_type: string; access_count: number }>>; entries: Array<{ id: string; key: string; value: Record<string, unknown>; memory_type: string; access_count: number }> }
  planner_activity: Array<{ id: string; message: string; detail: string; created_at: string }>
  timeline: Array<{ label: string; status: string }>
  chart_points: Array<{ label: string; value: number }>
  api_status: Array<{ label: string; state: string; detail: string }>
  command_palette_actions: Array<{ label: string; shortcut: string }>
  workflow_graph: WorkflowGraph
  workflow_template: { id: string; name: string; graph_data: WorkflowGraph }
  memory_hit_rate: number
}

const companyA: CompanyCard = {
  id: 'stripe',
  name: 'Stripe',
  domain: 'stripe.com',
  industry: 'FinTech / Payments',
  employee_count: 8000,
  revenue_usd: 14000000000,
  location: 'San Francisco, CA',
  icp_score: 96,
  confidence: 0.98,
  logo_color: '#635bff',
  tech_stack: ['React', 'Go', 'Kafka', 'PostgreSQL', 'AWS'],
  decision_makers: [
    { name: 'Patrick Collison', title: 'CEO & Co-Founder', email: 'patrick@stripe.com' },
    { name: 'Claire Hughes Johnson', title: 'COO', email: 'claire@stripe.com' },
  ],
  recommendation: 'Prioritize Stripe for a high-confidence enterprise motion and route to executive outreach.',
  recommended_action: 'Prioritize outreach',
  news_snippet: 'Stripe expands enterprise AI fraud tooling and hiring across platform teams.',
  growth_signals: ['Hiring acceleration', 'New AI product line', 'Enterprise growth'],
}

const companyB: CompanyCard = {
  id: 'vercel',
  name: 'Vercel',
  domain: 'vercel.com',
  industry: 'Cloud Infrastructure',
  employee_count: 400,
  revenue_usd: 110000000,
  location: 'San Francisco, CA',
  icp_score: 91,
  confidence: 0.96,
  logo_color: '#ffffff',
  tech_stack: ['React', 'Next.js', 'TypeScript', 'Edge Functions', 'Go'],
  decision_makers: [
    { name: 'Guillermo Rauch', title: 'CEO & Founder', email: 'rauch@vercel.com' },
    { name: 'Malte Ubl', title: 'CTO', email: 'malte@vercel.com' },
  ],
  recommendation: 'Strong fit for fast-moving technical teams with product-led growth motions.',
  recommended_action: 'Book discovery call',
  news_snippet: 'Vercel accelerates enterprise adoption with AI-powered UI generation.',
  growth_signals: ['Enterprise expansion', 'New AI product', 'Platform adoption'],
}

const companyC: CompanyCard = {
  id: 'figma',
  name: 'Figma',
  domain: 'figma.com',
  industry: 'Design SaaS',
  employee_count: 1200,
  revenue_usd: 400000000,
  location: 'San Francisco, CA',
  icp_score: 89,
  confidence: 0.95,
  logo_color: '#f24e1e',
  tech_stack: ['React', 'TypeScript', 'WebAssembly', 'GCP'],
  decision_makers: [
    { name: 'Dylan Field', title: 'CEO & Co-Founder', email: 'dylan@figma.com' },
    { name: 'Evan Wallace', title: 'CTO & Co-Founder', email: 'evan@figma.com' },
  ],
  recommendation: 'Prioritize with a focus on platform expansion and collaboration workflows.',
  recommended_action: 'Nurture with tailored sequence',
  news_snippet: 'Figma ships AI-assisted design workflows and enterprise security enhancements.',
  growth_signals: ['AI features', 'Enterprise upsell', 'APAC expansion'],
}

const graph: WorkflowGraph = {
  nodes: [
    { id: 'planner', type: 'agent', position: { x: 0, y: 0 }, data: { label: 'Planner', description: 'Reads memory and builds the plan.', category: 'orchestration', icon: 'brain', color: '#8b5cf6' } },
    { id: 'search', type: 'agent', position: { x: 260, y: 0 }, data: { label: 'Search', description: 'Finds candidate companies.', category: 'discovery', icon: 'search', color: '#06b6d4' } },
    { id: 'validate', type: 'agent', position: { x: 520, y: 0 }, data: { label: 'Validate', description: 'Removes stale or duplicate companies.', category: 'validation', icon: 'shield-check', color: '#10b981' } },
    { id: 'icp', type: 'agent', position: { x: 780, y: 0 }, data: { label: 'ICP', description: 'Scores accounts against the target profile.', category: 'analysis', icon: 'target', color: '#f59e0b' } },
    { id: 'decision', type: 'agent', position: { x: 0, y: 180 }, data: { label: 'Decision Maker', description: 'Finds executive contacts.', category: 'contacts', icon: 'users', color: '#a78bfa' } },
    { id: 'enrich', type: 'agent', position: { x: 260, y: 180 }, data: { label: 'Enrichment', description: 'Adds firmographic detail.', category: 'enrichment', icon: 'badge-plus', color: '#38bdf8' } },
    { id: 'summary', type: 'agent', position: { x: 520, y: 180 }, data: { label: 'Summary', description: 'Writes executive summaries.', category: 'synthesis', icon: 'file-text', color: '#f97316' } },
    { id: 'approval', type: 'agent', position: { x: 780, y: 180 }, data: { label: 'Approval', description: 'Waits for human review.', category: 'governance', icon: 'hand', color: '#eab308' } },
  ],
  edges: [
    { id: 'e1', source: 'planner', target: 'search', animated: true },
    { id: 'e2', source: 'search', target: 'validate', animated: true },
    { id: 'e3', source: 'validate', target: 'icp', animated: true },
    { id: 'e4', source: 'icp', target: 'decision', animated: true },
    { id: 'e5', source: 'decision', target: 'enrich', animated: true },
    { id: 'e6', source: 'enrich', target: 'summary', animated: true },
    { id: 'e7', source: 'summary', target: 'approval', animated: true },
  ],
  viewport: { x: 0, y: 0, zoom: 1 },
}

export const fallbackBootstrap: BootstrapData = {
  metrics: {
    total_workflows: 18,
    total_runs: 34,
    successful_runs: 31,
    failed_runs: 3,
    success_rate: 91.2,
    total_tokens_used: 124880,
    total_cost_usd: 42.18,
    avg_execution_time_ms: 18420,
    active_agents_count: 16,
    memory_hit_rate: 86.7,
    pending_approvals: 1,
    companies_discovered: 87,
  },
  workflow_status: { live_runs: 1, paused_runs: 1, completed_today: 6, pending_approvals: 1 },
  planner: {
    stage: 'Reading memory',
    message: 'Planner is analyzing request, consulting shared memory, and selecting the minimum viable agent graph.',
    reasoning: [
      'Reading shared memory to avoid duplicate outreach.',
      'Selecting only the agents required for the workflow objective.',
      'Preparing a human-in-the-loop checkpoint before any recommendation is finalized.',
    ],
  },
  projects: [{ id: 'project-1', name: 'Prospect Intelligence', description: 'B2B customer discovery workspace.', color: '#6366f1', icon: 'sparkles', workflow_count: 3 }],
  workflows: [
    {
      id: 'workflow-1',
      name: 'Customer Discovery Orchestration',
      description: 'Monitor news, validate companies, match ICP, and prepare approvals.',
      status: 'active',
      version: 4,
      graph_data: graph,
    },
  ],
  running_jobs: [
    { id: 'run-1', name: 'Customer Discovery Orchestration', status: 'running', progress: 68, current_step: 'Decision Maker Finder', planner_message: 'Identifying executive stakeholders.', total_tokens: 4820 },
    { id: 'run-2', name: 'Weekly Prospect Sweep', status: 'paused', progress: 78, current_step: 'Human Approval Agent', planner_message: 'Human review required before the shortlist is finalized.', total_tokens: 3990 },
  ],
  recent_runs: [
    { id: 'run-1', name: 'Customer Discovery Orchestration', status: 'running', progress: 68, current_step: 'Decision Maker Finder', planner_message: 'Identifying executive stakeholders.', total_tokens: 4820 },
    { id: 'run-2', name: 'Weekly Prospect Sweep', status: 'paused', progress: 78, current_step: 'Human Approval Agent', planner_message: 'Human review required before the shortlist is finalized.', total_tokens: 3990 },
  ],
  agents: [
    { id: 'planner_agent', name: 'Planner Agent', description: 'Builds the execution graph.', category: 'orchestration', capabilities: ['planning'], icon: 'brain', color: '#8b5cf6', success_rate: 0.98, avg_token_usage: 820, avg_execution_ms: 420 },
    { id: 'search_agent', name: 'Search Agent', description: 'Finds target companies.', category: 'discovery', capabilities: ['search'], icon: 'search', color: '#06b6d4', success_rate: 0.96, avg_token_usage: 640, avg_execution_ms: 540 },
  ],
  companies: [companyA, companyB, companyC],
  approvals: [
    {
      id: 'approval-1',
      run_id: 'run-2',
      agent_id: 'human_approval_agent',
      title: 'Approve prospect shortlist',
      status: 'pending',
      content: {
        headline: 'Three accounts are ready for human review',
        summary: 'The planner produced a shortlist with contact intelligence and a recommended outreach plan.',
        companies: [companyA, companyB, companyC],
      },
    },
  ],
  reports: [
    { id: 'report-1', run_id: 'run-2', title: 'B2B Customer Discovery Report', format: 'markdown', shareable_url: '/share/demo-report', created_at: new Date().toISOString() },
  ],
  notifications: [
    { id: 'note-1', type: 'workflow_completed', title: 'Workflow completed', message: 'The latest shortlist is ready for export.', read: false, created_at: new Date().toISOString() },
    { id: 'note-2', type: 'approval_required', title: 'Approval required', message: 'Human review is required before the recommendation is finalized.', read: false, created_at: new Date().toISOString() },
  ],
  memory: {
    total_entries: 4,
    groups: {
      planner: [{ id: 'm1', key: 'planner.duplicate.prevention', value: { blocked_domains: ['stripe.com'] }, memory_type: 'planner', access_count: 7 }],
      user_pref: [{ id: 'm2', key: 'user.preference.industry', value: { industries: ['SaaS', 'Cloud Infrastructure'] }, memory_type: 'user_pref', access_count: 14 }],
      workflow: [{ id: 'm3', key: 'workflow.run-2.summary', value: { companies: ['Stripe', 'Vercel', 'Figma'] }, memory_type: 'workflow', access_count: 1 }],
    },
    entries: [
      { id: 'm1', key: 'planner.duplicate.prevention', value: { blocked_domains: ['stripe.com'] }, memory_type: 'planner', access_count: 7 },
      { id: 'm2', key: 'user.preference.industry', value: { industries: ['SaaS', 'Cloud Infrastructure'] }, memory_type: 'user_pref', access_count: 14 },
      { id: 'm3', key: 'workflow.run-2.summary', value: { companies: ['Stripe', 'Vercel', 'Figma'] }, memory_type: 'workflow', access_count: 1 },
      { id: 'm4', key: 'search.last.query', value: { term: 'enterprise saas growth signals' }, memory_type: 'search', access_count: 3 },
    ],
  },
  planner_activity: [
    { id: 'p1', message: 'Planner completed a memory review.', detail: 'Prior results were used to avoid duplicate enrichment.', created_at: new Date().toISOString() },
    { id: 'p2', message: 'Planner started a new execution.', detail: 'A new customer discovery flow launched in demo mode.', created_at: new Date().toISOString() },
  ],
  timeline: [
    { label: 'Planning', status: 'complete' },
    { label: 'Discovery', status: 'complete' },
    { label: 'Validation', status: 'complete' },
    { label: 'Approval', status: 'live' },
  ],
  chart_points: [
    { label: 'Mon', value: 24 },
    { label: 'Tue', value: 32 },
    { label: 'Wed', value: 29 },
    { label: 'Thu', value: 45 },
    { label: 'Fri', value: 52 },
    { label: 'Sat', value: 60 },
    { label: 'Sun', value: 58 },
  ],
  api_status: [
    { label: 'FastAPI', state: 'online', detail: 'Demo API responding' },
    { label: 'Redis', state: 'optional', detail: 'Using in-memory fallback' },
    { label: 'WebSocket', state: 'live', detail: 'Planner events streaming' },
  ],
  command_palette_actions: [
    { label: 'Launch demo workflow', shortcut: 'Enter' },
    { label: 'Create workflow', shortcut: 'Ctrl+N' },
    { label: 'Open reports', shortcut: 'R' },
    { label: 'Toggle memory viewer', shortcut: 'M' },
  ],
  workflow_graph: graph,
  workflow_template: { id: 'workflow-1', name: 'Customer Discovery Orchestration', graph_data: graph },
  memory_hit_rate: 86.7,
}