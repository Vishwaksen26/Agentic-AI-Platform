"""Agent registry and workflow template definitions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import floor


@dataclass(frozen=True, slots=True)
class AgentSpec:
    id: str
    name: str
    description: str
    category: str
    capabilities: list[str]
    icon: str
    color: str
    avg_token_usage: int
    avg_execution_ms: int
    success_rate: float


AGENT_SPECS: list[AgentSpec] = [
    AgentSpec("planner_agent", "Planner Agent", "Analyzes goals, reads memory, and builds the execution graph.", "orchestration", ["planning", "memory", "orchestration"], "brain", "#8b5cf6", 820, 420, 0.98),
    AgentSpec("search_agent", "Search Agent", "Finds target companies across news, directories, and signals.", "discovery", ["search", "signal extraction", "company discovery"], "search", "#06b6d4", 640, 540, 0.96),
    AgentSpec("company_validation_agent", "Company Validation Agent", "Validates company quality and removes low-confidence entities.", "validation", ["validation", "deduplication", "quality control"], "shield-check", "#10b981", 450, 380, 0.97),
    AgentSpec("icp_matching_agent", "ICP Matching Agent", "Scores companies against the ideal customer profile.", "analysis", ["scoring", "icp", "fit analysis"], "target", "#f59e0b", 520, 450, 0.95),
    AgentSpec("market_intelligence_agent", "Market Intelligence Agent", "Reads growth signals, news, and competitive positioning.", "intelligence", ["news", "growth signals", "market analysis"], "newspaper", "#fb7185", 560, 500, 0.94),
    AgentSpec("company_enrichment_agent", "Company Enrichment Agent", "Adds funding, tech stack, and firmographic detail.", "enrichment", ["firmographics", "funding", "technology"], "badge-plus", "#38bdf8", 700, 560, 0.96),
    AgentSpec("decision_maker_finder", "Decision Maker Finder", "Identifies executive contacts and buying committee members.", "contacts", ["contacts", "buying committee", "org chart"], "users", "#a78bfa", 620, 520, 0.95),
    AgentSpec("linkedin_agent", "LinkedIn Agent", "Enriches people with LinkedIn profiles and social context.", "contacts", ["linkedin", "people enrichment"], "linkedin", "#0ea5e9", 360, 300, 0.93),
    AgentSpec("email_enrichment_agent", "Email Enrichment Agent", "Discovers and verifies business email addresses.", "contacts", ["email discovery", "verification"], "mail", "#14b8a6", 420, 340, 0.94),
    AgentSpec("phone_enrichment_agent", "Phone Enrichment Agent", "Finds phone numbers and direct lines for outreach.", "contacts", ["phone discovery", "verification"], "phone", "#22c55e", 300, 260, 0.92),
    AgentSpec("summary_agent", "Summary Agent", "Writes concise executive summaries for each account.", "synthesis", ["summarization", "narrative"], "file-text", "#f97316", 540, 420, 0.97),
    AgentSpec("recommendation_agent", "Recommendation Agent", "Ranks the best next action for the sales team.", "synthesis", ["prioritization", "recommendations"], "sparkles", "#ef4444", 620, 430, 0.95),
    AgentSpec("human_approval_agent", "Human Approval Agent", "Pauses the workflow for review and governance.", "governance", ["approval", "review", "audit trail"], "hand", "#eab308", 180, 220, 1.0),
    AgentSpec("report_generator", "Report Generator", "Produces PDF, CSV, Markdown, and shareable report artifacts.", "output", ["reporting", "exports"], "file-output", "#6366f1", 480, 360, 0.98),
    AgentSpec("memory_agent", "Memory Agent", "Writes execution history and learned context into shared memory.", "memory", ["memory write", "dedupe", "context retrieval"], "database", "#84cc16", 320, 280, 0.97),
    AgentSpec("analytics_agent", "Analytics Agent", "Captures usage, efficiency, and conversion metrics.", "analytics", ["metrics", "monitoring", "trends"], "bar-chart-3", "#14b8a6", 260, 240, 0.99),
]

AGENT_LOOKUP = {spec.id: spec for spec in AGENT_SPECS}
EXECUTION_SEQUENCE = [spec.id for spec in AGENT_SPECS]


def agent_info_list() -> list[dict]:
    return [
        {
            **asdict(spec),
            "capabilities": list(spec.capabilities),
        }
        for spec in AGENT_SPECS
    ]


def build_default_workflow_graph() -> dict:
    nodes: list[dict] = []
    edges: list[dict] = []

    for index, spec in enumerate(AGENT_SPECS):
        column = index % 4
        row = floor(index / 4)
        nodes.append(
            {
                "id": spec.id,
                "type": "agent",
                "position": {"x": column * 260, "y": row * 180},
                "data": {
                    "id": spec.id,
                    "label": spec.name,
                    "description": spec.description,
                    "category": spec.category,
                    "icon": spec.icon,
                    "color": spec.color,
                },
                "style": {
                    "background": "rgba(17, 17, 24, 0.96)",
                    "border": f"1px solid {spec.color}",
                    "borderRadius": 18,
                    "color": "#f4f4f8",
                    "width": 230,
                    "boxShadow": "0 16px 36px rgba(0, 0, 0, 0.35)",
                },
            }
        )

        if index < len(AGENT_SPECS) - 1:
            edges.append(
                {
                    "id": f"{spec.id}-{AGENT_SPECS[index + 1].id}",
                    "source": spec.id,
                    "target": AGENT_SPECS[index + 1].id,
                    "animated": True,
                    "style": {"stroke": spec.color, "strokeWidth": 2},
                }
            )

    return {
        "nodes": nodes,
        "edges": edges,
        "viewport": {"x": 0, "y": 0, "zoom": 0.9},
    }