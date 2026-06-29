import { useEffect, useMemo, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import {
  ArrowRight,
  BarChart3,
  Brain,
  Command,
  Download,
  Layers3,
  Mail,
  Play,
  RefreshCcw,
  Search,
  ShieldCheck,
  Sparkles,
  Wand2,
} from 'lucide-react'
import ReactFlow, { Background, Controls, Handle, MiniMap, Position, type NodeProps } from 'reactflow'
import 'reactflow/dist/style.css'
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import './App.css'
import { getJson, getWebSocketUrl, postJson } from './api'
import { fallbackBootstrap, type BootstrapData } from './demoData'

type LiveEvent = {
  id: string
  type: string
  title: string
  message: string
  timestamp: string
}

type PlannerNodeData = {
  label: string
  description: string
  category: string
  icon: string
  color: string
}

function PlannerNode({ data, selected }: NodeProps<PlannerNodeData>) {
  return (
    <div className={`planner-node ${selected ? 'planner-node--selected' : ''}`} style={{ borderColor: data.color }}>
      <Handle type="target" position={Position.Top} />
      <div className="planner-node__icon" style={{ background: data.color }}>
        {data.icon.slice(0, 1).toUpperCase()}
      </div>
      <div className="planner-node__content">
        <div className="planner-node__category">{data.category}</div>
        <div className="planner-node__label">{data.label}</div>
        <div className="planner-node__description">{data.description}</div>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}

function formatCurrency(amount: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(amount)
}

function formatCompactNumber(value: number) {
  return new Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 1 }).format(value)
}

function formatDuration(ms: number) {
  if (!ms) {
    return '0s'
  }

  if (ms < 1000) {
    return `${ms}ms`
  }

  return `${(ms / 1000).toFixed(1)}s`
}

function App() {
  const [bootstrap, setBootstrap] = useState<BootstrapData>(fallbackBootstrap)
  const [loading, setLoading] = useState(true)
  const [activeRunId, setActiveRunId] = useState<string | null>(null)
  const [selectedCompanyId, setSelectedCompanyId] = useState(fallbackBootstrap.companies[0]?.id ?? '')
  const [selectedApprovalId, setSelectedApprovalId] = useState(fallbackBootstrap.approvals[0]?.id ?? '')
  const [liveEvents, setLiveEvents] = useState<LiveEvent[]>([])
  const [commandOpen, setCommandOpen] = useState(false)
  const [commandQuery, setCommandQuery] = useState('')
  const [submittingApproval, setSubmittingApproval] = useState(false)

  const loadBootstrap = async () => {
    try {
      const snapshot = await getJson<BootstrapData>('/demo/bootstrap')
      setBootstrap(snapshot)
      setSelectedCompanyId((current) => current || snapshot.companies[0]?.id || '')
      setSelectedApprovalId((current) => current || snapshot.approvals[0]?.id || '')
    } catch {
      setBootstrap(fallbackBootstrap)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadBootstrap()
  }, [])

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
        event.preventDefault()
        setCommandOpen(true)
      }

      if (event.key === 'Escape') {
        setCommandOpen(false)
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [])

  useEffect(() => {
    if (!activeRunId) {
      return undefined
    }

    const socket = new WebSocket(getWebSocketUrl(`/ws/${activeRunId}`))

    socket.onmessage = (event) => {
      const payload = JSON.parse(event.data) as Record<string, unknown>
      const type = String(payload.type ?? 'event')
      const message = String(payload.message ?? payload.detail ?? '')
      const title = String(payload.agent_name ?? payload.step ?? payload.type ?? 'Update')

      setLiveEvents((current) => [
        {
          id: `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
          type,
          title,
          message,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
        ...current,
      ].slice(0, 14))

      if (type === 'approval_required') {
        void loadBootstrap()
        setSelectedApprovalId(String(payload.approval_id ?? selectedApprovalId))
      }

      if (type === 'workflow_completed') {
        void loadBootstrap()
      }
    }

    socket.onerror = () => {
      setLiveEvents((current) => [
        {
          id: `${Date.now()}-socket-error`,
          type: 'error',
          title: 'Realtime stream unavailable',
          message: 'The dashboard is falling back to the latest server snapshot.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        },
        ...current,
      ])
    }

    return () => socket.close()
  }, [activeRunId])

  const selectedCompany = bootstrap.companies.find((company) => company.id === selectedCompanyId) ?? bootstrap.companies[0]
  const selectedApproval = bootstrap.approvals.find((approval) => approval.id === selectedApprovalId) ?? bootstrap.approvals[0]
  const activeRun = bootstrap.running_jobs[0]
  const workflowGraph = bootstrap.workflow_graph

  const commandActions = useMemo(
    () =>
      bootstrap.command_palette_actions.map((action, index) => ({
        ...action,
        id: `${action.label}-${index}`,
      })),
    [bootstrap.command_palette_actions],
  )

  const filteredActions = commandActions.filter((action) =>
    `${action.label} ${action.shortcut}`.toLowerCase().includes(commandQuery.toLowerCase()),
  )

  const launchDemo = async () => {
    const workflowId = bootstrap.workflow_template.id ?? bootstrap.workflows[0]?.id
    if (!workflowId) {
      return
    }

    const result = await postJson<{ id: string }>('/demo/start', {
      workflow_id: workflowId,
      input_data: {
        objective: 'Discover and qualify enterprise prospects',
        segment: 'B2B SaaS',
        region: 'North America',
      },
    })

    setActiveRunId(result.id)
    setLiveEvents([])
    await loadBootstrap()
  }

  const submitApproval = async (decision: 'approved' | 'rejected' | 'edited') => {
    if (!selectedApproval) {
      return
    }

    setSubmittingApproval(true)
    try {
      await postJson(`/approvals/${selectedApproval.id}/decision`, {
        decision,
        comment:
          decision === 'approved'
            ? 'Approved for executive outreach.'
            : decision === 'edited'
              ? 'Adjusted shortlist to match the latest account review.'
              : 'The shortlist needs additional confidence before outreach.',
        edited_content:
          decision === 'edited'
            ? {
                headline: 'Adjusted shortlist after human review',
                summary: 'The human reviewer tuned the shortlist before final export.',
                companies: bootstrap.companies.slice(0, 3),
              }
            : undefined,
      })
      await loadBootstrap()
    } finally {
      setSubmittingApproval(false)
    }
  }

  const runState = activeRun ?? bootstrap.recent_runs[0]
  const plannerReasoning = bootstrap.planner.reasoning
  const runProgress = runState?.progress ?? 0
  const nodeTypes = useRef({
    agent: PlannerNode,
  }).current

  return (
    <div className="app-shell">
      <div className="bg-orb bg-orb--violet" />
      <div className="bg-orb bg-orb--cyan" />
      <div className="bg-orb bg-orb--amber" />

      <header className="topbar glass-panel">
        <div className="topbar__brand">
          <div className="brand-mark">
            <Brain size={18} />
          </div>
          <div>
            <div className="topbar__eyebrow">AgentForge AI</div>
            <div className="topbar__title">Enterprise agentic intelligence platform</div>
          </div>
        </div>

        <div className="topbar__actions">
          <button className="button button--ghost" type="button" onClick={() => setCommandOpen(true)}>
            <Command size={16} />
            Command palette
          </button>
          <button className="button button--ghost" type="button" onClick={() => void loadBootstrap()}>
            <RefreshCcw size={16} />
            Refresh
          </button>
          <button className="button button--primary" type="button" onClick={() => void launchDemo()}>
            <Play size={16} />
            Launch demo workflow
          </button>
        </div>
      </header>

      <main className="dashboard">
        <motion.section
          className="hero-panel glass-panel"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
        >
          <div className="hero-panel__content">
            <div className="hero-panel__badge">
              <Sparkles size={14} />
              One-click demo mode
            </div>
            <h1>Visual agent orchestration for enterprise prospect intelligence.</h1>
            <p>
              Build workflows, route execution through a planner, pause for human approval, and reuse memory across every prospecting run.
            </p>

            <div className="hero-panel__cta">
              <button className="button button--primary" type="button" onClick={() => void launchDemo()}>
                <Wand2 size={16} />
                Run 20-second demo
              </button>
              <button className="button button--ghost" type="button" onClick={() => setCommandOpen(true)}>
                <Layers3 size={16} />
                Open workflow builder
              </button>
            </div>

            <div className="hero-panel__meta">
              <span>Planner-aware orchestration</span>
              <span>Shared memory</span>
              <span>Human-in-the-loop review</span>
              <span>Realtime execution</span>
            </div>
          </div>

          <div className="hero-panel__side">
            <div className="hero-stat">
              <div className="hero-stat__label">Current stage</div>
              <div className="hero-stat__value">{bootstrap.planner.stage}</div>
              <div className="hero-stat__caption">{bootstrap.planner.message}</div>
              <div className="hero-progress">
                <div className="hero-progress__meta">
                  <span>Execution progress</span>
                  <strong>{runProgress}%</strong>
                </div>
                <div className="hero-progress__track">
                  <div className="hero-progress__fill" style={{ width: `${runProgress}%` }} />
                </div>
              </div>
            </div>
            <div className="hero-stat-grid">
              <div className="hero-stat hero-stat--small">
                <div className="hero-stat__label">Live runs</div>
                <div className="hero-stat__value">{bootstrap.workflow_status.live_runs}</div>
              </div>
              <div className="hero-stat hero-stat--small">
                <div className="hero-stat__label">Approvals</div>
                <div className="hero-stat__value">{bootstrap.workflow_status.pending_approvals}</div>
              </div>
            </div>
          </div>
        </motion.section>

        <section className="metrics-grid">
          {[
            { label: 'Success rate', value: `${bootstrap.metrics.success_rate.toFixed(1)}%`, icon: ShieldCheck },
            { label: 'Execution time', value: formatDuration(bootstrap.metrics.avg_execution_time_ms), icon: BarChart3 },
            { label: 'Active agents', value: String(bootstrap.metrics.active_agents_count), icon: Sparkles },
            { label: 'Memory hit rate', value: `${bootstrap.metrics.memory_hit_rate.toFixed(1)}%`, icon: Brain },
            { label: 'Companies discovered', value: formatCompactNumber(bootstrap.metrics.companies_discovered), icon: Search },
            { label: 'Tokens used', value: formatCompactNumber(bootstrap.metrics.total_tokens_used), icon: Mail },
          ].map((metric, index) => (
            <motion.article
              key={metric.label}
              className="metric-card glass-panel"
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, delay: index * 0.05 }}
            >
              <metric.icon size={18} />
              <div>
                <div className="metric-card__label">{metric.label}</div>
                <div className="metric-card__value">{metric.value}</div>
              </div>
            </motion.article>
          ))}
        </section>

        <section className="main-grid">
          <div className="main-grid__left">
            <section className="section glass-panel planner-console">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Planner console</div>
                  <h2>Reasoning in natural language, not a spinner.</h2>
                </div>
                <div className={`status-chip status-chip--${runState?.status ?? 'idle'}`}>
                  <span className="status-dot" />
                  {runState?.status ?? 'idle'}
                </div>
              </div>

              <div className="planner-console__body">
                <div className="planner-console__stage">{bootstrap.planner.stage}</div>
                <p className="planner-console__message">{bootstrap.planner.message}</p>
                <div className="planner-console__list">
                  {plannerReasoning.map((line, index) => (
                    <motion.div
                      key={`${line}-${index}`}
                      className="planner-console__line"
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.25, delay: index * 0.05 }}
                    >
                      <span className="planner-console__bullet" />
                      <span>{line}</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            </section>

            <section className="section glass-panel workflow-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Workflow builder</div>
                  <h2>React Flow canvas for composable agent graphs.</h2>
                </div>
                <div className="section__actions">
                  <button className="button button--ghost button--sm" type="button" onClick={() => void launchDemo()}>
                    <Play size={14} />
                    Run
                  </button>
                  <button className="button button--ghost button--sm" type="button">
                    <Download size={14} />
                    Export
                  </button>
                </div>
              </div>

              <div className="workflow-canvas">
                <ReactFlow
                  nodes={workflowGraph.nodes}
                  edges={workflowGraph.edges}
                  nodeTypes={nodeTypes}
                  fitView
                  minZoom={0.55}
                  maxZoom={1.4}
                  proOptions={{ hideAttribution: true }}
                >
                  <MiniMap zoomable pannable />
                  <Controls />
                  <Background gap={20} size={1} />
                </ReactFlow>
              </div>
            </section>

            <section className="section glass-panel timeline-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Execution timeline</div>
                  <h2>Live progress with agent runtime, tokens, and logs.</h2>
                </div>
                <div className="section__meta">{runState ? `${runState.progress ?? 0}% complete` : 'Idle'}</div>
              </div>

              <div className="timeline-track">
                {bootstrap.timeline.map((step, index) => (
                  <div key={step.label} className={`timeline-item timeline-item--${step.status}`}>
                    <div className="timeline-item__dot" />
                    <div className="timeline-item__body">
                      <div className="timeline-item__label">{step.label}</div>
                      <div className="timeline-item__caption">
                        {index === 0 ? 'Planner is reading memory.' : step.status === 'live' ? 'Currently active.' : 'Completed.'}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="execution-log">
                {liveEvents.length ? (
                  liveEvents.map((event) => (
                    <div key={event.id} className="execution-log__row">
                      <div className="execution-log__time">{event.timestamp}</div>
                      <div className="execution-log__content">
                        <strong>{event.title}</strong>
                        <span>{event.message}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="execution-log__empty">Run the demo to stream planner and agent activity here.</div>
                )}
              </div>
            </section>

            <section className="section glass-panel runs-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Recent runs</div>
                  <h2>Most recent orchestration executions.</h2>
                </div>
                <div className="section__meta">{bootstrap.recent_runs.length} runs</div>
              </div>

              <div className="runs-list">
                {bootstrap.recent_runs.slice(0, 3).map((run) => (
                  <div key={run.id} className="run-row">
                    <div className="run-row__left">
                      <div className={`run-row__pill run-row__pill--${run.status}`}>{run.status}</div>
                      <div>
                        <div className="run-row__title">{run.name}</div>
                        <div className="run-row__detail">{run.current_step}</div>
                      </div>
                    </div>
                    <div className="run-row__right">
                      <strong>{run.progress}%</strong>
                      <span>{formatCompactNumber(run.total_tokens)} tokens</span>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>

          <aside className="main-grid__right">
            <section className="section glass-panel company-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Company cards</div>
                  <h2>Qualified prospects, enriched for outreach.</h2>
                </div>
                <div className="section__meta">Top {bootstrap.companies.length}</div>
              </div>

              <div className="company-grid">
                {bootstrap.companies.map((company) => (
                  <button
                    key={company.id}
                    type="button"
                    className={`company-card ${selectedCompanyId === company.id ? 'company-card--selected' : ''}`}
                    onClick={() => setSelectedCompanyId(company.id)}
                  >
                    <div className="company-card__header">
                      <div className="company-card__logo" style={{ background: company.logo_color }}>
                        {company.name.slice(0, 1)}
                      </div>
                      <div>
                        <div className="company-card__name">{company.name}</div>
                        <div className="company-card__meta">{company.industry}</div>
                      </div>
                    </div>
                    <div className="company-card__stats">
                      <span>{company.employee_count.toLocaleString()} employees</span>
                      <span>{formatCurrency(company.revenue_usd)}</span>
                    </div>
                    <div className="company-card__score">
                      <span>ICP match</span>
                      <strong>{company.icp_score}%</strong>
                    </div>
                  </button>
                ))}
              </div>

              {selectedCompany ? (
                <div className="company-detail">
                  <div className="company-detail__title">
                    <h3>{selectedCompany.name}</h3>
                    <span>{selectedCompany.recommended_action}</span>
                  </div>
                  <p>{selectedCompany.recommendation}</p>
                  <div className="company-detail__grid">
                    <div>
                      <span>Location</span>
                      <strong>{selectedCompany.location}</strong>
                    </div>
                    <div>
                      <span>Confidence</span>
                      <strong>{Math.round(selectedCompany.confidence * 100)}%</strong>
                    </div>
                    <div>
                      <span>Decision makers</span>
                      <strong>{selectedCompany.decision_makers.length}</strong>
                    </div>
                    <div>
                      <span>Stack</span>
                      <strong>{selectedCompany.tech_stack.slice(0, 3).join(', ')}</strong>
                    </div>
                  </div>
                </div>
              ) : null}
            </section>

            <section className="section glass-panel approval-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Human approval</div>
                  <h2>Approve, reject, or edit the shortlist.</h2>
                </div>
                <div className={`status-chip status-chip--${selectedApproval?.status ?? 'pending'}`}>
                  <span className="status-dot" />
                  {selectedApproval?.status ?? 'pending'}
                </div>
              </div>

              {selectedApproval ? (
                <div className="approval-card">
                  <h3>{selectedApproval.title}</h3>
                  <p>{selectedApproval.content.summary}</p>
                  <div className="approval-card__actions">
                    <button className="button button--primary button--sm" type="button" disabled={submittingApproval} onClick={() => void submitApproval('approved')}>
                      Approve
                    </button>
                    <button className="button button--ghost button--sm" type="button" disabled={submittingApproval} onClick={() => void submitApproval('edited')}>
                      Edit
                    </button>
                    <button className="button button--ghost button--sm" type="button" disabled={submittingApproval} onClick={() => void submitApproval('rejected')}>
                      Reject
                    </button>
                  </div>
                </div>
              ) : (
                <div className="empty-state">Start the demo workflow to create an approval task.</div>
              )}
            </section>

            <section className="section glass-panel analytics-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Analytics</div>
                  <h2>Workflow health and token usage.</h2>
                </div>
              </div>

              <div className="chart-wrap">
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={bootstrap.chart_points} margin={{ top: 10, right: 16, left: -10, bottom: 0 }}>
                    <XAxis dataKey="label" tickLine={false} axisLine={false} stroke="rgba(255,255,255,0.35)" />
                    <YAxis hide />
                    <Tooltip
                      contentStyle={{
                        background: 'rgba(10, 10, 15, 0.96)',
                        border: '1px solid rgba(255,255,255,0.08)',
                        borderRadius: '14px',
                        color: '#f4f4f8',
                      }}
                    />
                    <Line type="monotone" dataKey="value" stroke="#7c3aed" strokeWidth={3} dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="analytics-summary">
                <div>
                  <span>Token usage</span>
                  <strong>{formatCompactNumber(bootstrap.metrics.total_tokens_used)}</strong>
                </div>
                <div>
                  <span>Cost</span>
                  <strong>{formatCurrency(bootstrap.metrics.total_cost_usd)}</strong>
                </div>
                <div>
                  <span>Execution time</span>
                  <strong>{formatDuration(bootstrap.metrics.avg_execution_time_ms)}</strong>
                </div>
              </div>
            </section>

            <section className="section glass-panel memory-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Memory viewer</div>
                  <h2>Planner memory, search history, and workflow context.</h2>
                </div>
                <div className="section__meta">{bootstrap.memory.total_entries} entries</div>
              </div>

              <div className="memory-groups">
                {Object.entries(bootstrap.memory.groups).map(([group, entries]) => (
                  <div key={group} className="memory-group">
                    <div className="memory-group__label">{group}</div>
                    <div className="memory-group__count">{entries.length}</div>
                  </div>
                ))}
              </div>

              <div className="memory-list">
                {bootstrap.memory.entries.slice(0, 4).map((entry) => (
                  <div key={entry.id} className="memory-list__item">
                    <div className="memory-list__key">{entry.key}</div>
                    <div className="memory-list__meta">{entry.memory_type} · {entry.access_count} accesses</div>
                  </div>
                ))}
              </div>
            </section>

            <section className="section glass-panel reports-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">Reports</div>
                  <h2>Exportable report artifacts.</h2>
                </div>
              </div>

              <div className="reports-list">
                {bootstrap.reports.map((report) => (
                  <div key={report.id} className="report-row">
                    <div>
                      <div className="report-row__title">{report.title}</div>
                      <div className="report-row__meta">{report.format.toUpperCase()} · {report.shareable_url ?? 'private'}</div>
                    </div>
                    <a className="report-row__link" href={report.shareable_url ?? '#'} target="_blank" rel="noreferrer">
                      <ArrowRight size={14} />
                    </a>
                  </div>
                ))}
              </div>
            </section>

            <section className="section glass-panel api-section">
              <div className="section__header">
                <div>
                  <div className="section__eyebrow">API status</div>
                  <h2>Live platform services.</h2>
                </div>
              </div>

              <div className="api-list">
                {bootstrap.api_status.map((item) => (
                  <div key={item.label} className="api-row">
                    <div>
                      <div className="api-row__label">{item.label}</div>
                      <div className="api-row__detail">{item.detail}</div>
                    </div>
                    <div className={`api-row__state api-row__state--${item.state}`}>{item.state}</div>
                  </div>
                ))}
              </div>
            </section>
          </aside>
        </section>

        <section className="section glass-panel feed-section">
          <div className="section__header">
            <div>
              <div className="section__eyebrow">Planner activity</div>
              <h2>Recent reasoning and execution decisions.</h2>
            </div>
            <div className="section__meta">{loading ? 'Loading...' : 'Synced'}</div>
          </div>

          <div className="feed-grid">
            {bootstrap.planner_activity.map((item) => (
              <div key={item.id} className="feed-card">
                <div className="feed-card__title">{item.message}</div>
                <div className="feed-card__detail">{item.detail}</div>
                <div className="feed-card__time">{new Date(item.created_at).toLocaleString()}</div>
              </div>
            ))}
          </div>
        </section>
      </main>

      <AnimatePresence>
        {commandOpen ? (
          <motion.div className="command-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <motion.div className="command-palette glass-panel" initial={{ opacity: 0, y: 12, scale: 0.98 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 12, scale: 0.98 }}>
              <div className="command-palette__header">
                <Command size={16} />
                <input
                  autoFocus
                  value={commandQuery}
                  onChange={(event) => setCommandQuery(event.target.value)}
                  placeholder="Search workflows, reports, and actions..."
                />
              </div>

              <div className="command-palette__list">
                {filteredActions.map((action) => (
                  <button
                    key={action.id}
                    type="button"
                    className="command-item"
                    onClick={async () => {
                      if (action.label.toLowerCase().includes('launch')) {
                        await launchDemo()
                      }
                      if (action.label.toLowerCase().includes('report')) {
                        document.querySelector('.reports-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
                      }
                      if (action.label.toLowerCase().includes('memory')) {
                        document.querySelector('.memory-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
                      }
                      setCommandOpen(false)
                    }}
                  >
                    <span>{action.label}</span>
                    <kbd>{action.shortcut}</kbd>
                  </button>
                ))}
                {!filteredActions.length ? <div className="command-item command-item--empty">No actions match your search.</div> : null}
              </div>
            </motion.div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </div>
  )
}

export default App