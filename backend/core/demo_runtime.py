"""In-memory demo runtime for AgentForge AI.

The runtime keeps the app fully runnable in demo mode without external services.
It simulates planner reasoning, agent execution, approvals, reports, analytics,
and shared memory while broadcasting live WebSocket events.
"""

from __future__ import annotations

import asyncio
import copy
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from backend.agents.demo_data import ICP_CRITERIA, SAMPLE_COMPANIES, SAMPLE_DECISION_MAKERS
from backend.agents.registry import AGENT_SPECS, build_default_workflow_graph, agent_info_list
from backend.core.websocket_manager import ws_manager


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime | None = None) -> str:
    return (value or _now()).isoformat()


def _slug(value: str) -> str:
    return value.lower().replace(" ", "-")


def _company_score(company: dict[str, Any]) -> tuple[float, float, list[str]]:
    score = 0.0
    reasons: list[str] = []

    if company["industry"] in ICP_CRITERIA["industry"]:
        score += 30
        reasons.append("Industry matches ICP")

    if ICP_CRITERIA["min_employees"] <= company["employee_count"] <= ICP_CRITERIA["max_employees"]:
        score += 20
        reasons.append("Firmographic size is in range")

    if company["revenue_usd"] >= ICP_CRITERIA["min_revenue_usd"]:
        score += 20
        reasons.append("Revenue clears threshold")

    tech_alignment = len({tech for tech in company["tech_stack"] if tech in ICP_CRITERIA["tech_requirements"]})
    if tech_alignment:
        score += 15
        reasons.append("Tech stack aligns with buyer profile")

    if len(company.get("growth_signals", [])) >= 2:
        score += 15
        reasons.append("Clear growth signals detected")

    score = min(score, 98.0)
    confidence = min(0.99, 0.55 + score / 180)
    return score, confidence, reasons


@dataclass
class DemoRuntime:
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    projects: list[dict[str, Any]] = field(default_factory=list)
    workflows: list[dict[str, Any]] = field(default_factory=list)
    runs: dict[str, dict[str, Any]] = field(default_factory=dict)
    approvals: dict[str, dict[str, Any]] = field(default_factory=dict)
    reports: list[dict[str, Any]] = field(default_factory=list)
    notifications: list[dict[str, Any]] = field(default_factory=list)
    memory_entries: list[dict[str, Any]] = field(default_factory=list)
    planner_activity: list[dict[str, Any]] = field(default_factory=list)
    run_tasks: dict[str, asyncio.Task] = field(default_factory=dict)

    def __post_init__(self):
        self._seed()

    def _seed(self):
        project_id = str(uuid.uuid4())
        workflow_id = str(uuid.uuid4())
        now = _now()

        self.projects = [
            {
                "id": project_id,
                "name": "Prospect Intelligence",
                "description": "B2B customer discovery and lead qualification for enterprise sales teams.",
                "color": "#6366f1",
                "icon": "sparkles",
                "owner_id": "demo-user",
                "created_at": _iso(now),
                "workflow_count": 1,
            }
        ]

        self.workflows = [
            {
                "id": workflow_id,
                "name": "Customer Discovery Orchestration",
                "description": "Monitor market signals, validate companies, enrich contacts, and route to human review.",
                "version": 4,
                "status": "active",
                "graph_data": build_default_workflow_graph(),
                "agent_config": {spec.id: {"enabled": True, "priority": index + 1} for index, spec in enumerate(AGENT_SPECS)},
                "tags": ["demo", "b2b", "prospect-intelligence"],
                "project_id": project_id,
                "owner_id": "demo-user",
                "created_at": _iso(now),
                "updated_at": _iso(now),
                "run_count": 3,
                "last_run_status": "completed",
            }
        ]

        self.memory_entries = [
            {
                "id": str(uuid.uuid4()),
                "key": "user.preference.industry",
                "value": {"industries": ["SaaS", "Cloud Infrastructure", "FinTech"]},
                "memory_type": "user_pref",
                "source_run_id": None,
                "access_count": 14,
                "last_accessed": _iso(now),
                "created_at": _iso(now),
            },
            {
                "id": str(uuid.uuid4()),
                "key": "planner.duplicate.prevention",
                "value": {"blocked_domains": ["stripe.com", "notion.so"]},
                "memory_type": "planner",
                "source_run_id": None,
                "access_count": 7,
                "last_accessed": _iso(now),
                "created_at": _iso(now),
            },
        ]

        self.notifications = [
            {
                "id": str(uuid.uuid4()),
                "type": "workflow_completed",
                "title": "Demo workflow ready",
                "message": "Customer discovery workflow is configured and ready for one-click execution.",
                "read": False,
                "metadata": {"workflow_id": workflow_id},
                "created_at": _iso(now),
            }
        ]

        self.reports = [
            {
                "id": str(uuid.uuid4()),
                "run_id": None,
                "title": "Weekly Prospect Intelligence Brief",
                "format": "markdown",
                "file_path": "/reports/demo/prospect-intelligence.md",
                "shareable_url": "/share/demo/prospect-intelligence",
                "created_at": _iso(now),
            }
        ]

        self.planner_activity = [
            {
                "id": str(uuid.uuid4()),
                "message": "Planner primed memory and loaded the customer discovery template.",
                "detail": "Reads memory before every workflow stage to avoid duplicate outreach.",
                "created_at": _iso(now),
            }
        ]

    def _active_workflow(self) -> dict[str, Any]:
        return self.workflows[0]

    def _top_companies(self) -> list[dict[str, Any]]:
        companies: list[dict[str, Any]] = []
        for sample in SAMPLE_COMPANIES:
            score, confidence, reasons = _company_score(sample)
            enriched = copy.deepcopy(sample)
            enriched["icp_score"] = round(score, 1)
            enriched["confidence"] = round(confidence, 2)
            enriched["reasoning"] = reasons
            enriched["decision_makers"] = SAMPLE_DECISION_MAKERS.get(sample["name"], [])
            enriched["recommended_action"] = "Prioritize outreach" if score >= 85 else "Review manually" if score >= 70 else "Monitor"
            enriched["recommendation"] = f"{sample['name']} is a strong fit with {int(score)} ICP score and {len(enriched['decision_makers'])} reachable decision makers."
            companies.append(enriched)

        companies.sort(key=lambda item: (item["icp_score"], item["confidence"]), reverse=True)
        return companies[:5]

    def _record_notification(self, notification_type: str, title: str, message: str, metadata: dict[str, Any] | None = None):
        notification = {
            "id": str(uuid.uuid4()),
            "type": notification_type,
            "title": title,
            "message": message,
            "read": False,
            "metadata": metadata or {},
            "created_at": _iso(),
        }
        self.notifications.insert(0, notification)
        return notification

    def _record_planner_activity(self, message: str, detail: str):
        activity = {
            "id": str(uuid.uuid4()),
            "message": message,
            "detail": detail,
            "created_at": _iso(),
        }
        self.planner_activity.insert(0, activity)
        return activity

    def _get_run(self, run_id: str) -> dict[str, Any]:
        if run_id not in self.runs:
            raise KeyError(run_id)
        return self.runs[run_id]

    def _serialize_run(self, run: dict[str, Any]) -> dict[str, Any]:
        serialized = {key: value for key, value in run.items() if key != "approval_event"}
        serialized["current_step"] = serialized.get("current_step", "")
        return serialized

    def list_agents(self) -> list[dict[str, Any]]:
        return agent_info_list()

    def list_workflows(self) -> list[dict[str, Any]]:
        return [copy.deepcopy(workflow) for workflow in self.workflows]

    def get_workflow(self, workflow_id: str) -> dict[str, Any]:
        for workflow in self.workflows:
            if workflow["id"] == workflow_id:
                return copy.deepcopy(workflow)
        raise KeyError(workflow_id)

    def get_run(self, run_id: str) -> dict[str, Any]:
        return self._serialize_run(self._get_run(run_id))

    def get_approvals(self) -> list[dict[str, Any]]:
        return list(self.approvals.values())

    def get_reports(self) -> list[dict[str, Any]]:
        return [copy.deepcopy(report) for report in self.reports]

    def get_notifications(self) -> list[dict[str, Any]]:
        return [copy.deepcopy(notification) for notification in self.notifications]

    def get_memory_entries(self) -> list[dict[str, Any]]:
        return [copy.deepcopy(entry) for entry in self.memory_entries]

    def get_planner_activity(self) -> list[dict[str, Any]]:
        return [copy.deepcopy(item) for item in self.planner_activity]

    def get_analytics_summary(self) -> dict[str, Any]:
        completed_runs = [run for run in self.runs.values() if run["status"] == "completed"]
        failed_runs = [run for run in self.runs.values() if run["status"] == "failed"]
        pending_approvals = sum(1 for approval in self.approvals.values() if approval["status"] == "pending")
        total_tokens = sum(run.get("total_tokens", 0) for run in self.runs.values())
        total_cost = sum(run.get("total_cost_usd", 0.0) for run in self.runs.values())
        elapsed_values = [run.get("elapsed_ms", 0) for run in self.runs.values() if run.get("elapsed_ms")]

        return {
            "total_workflows": len(self.workflows),
            "total_runs": len(self.runs),
            "successful_runs": len(completed_runs),
            "failed_runs": len(failed_runs),
            "success_rate": round((len(completed_runs) / max(1, len(self.runs))) * 100, 1),
            "total_tokens_used": total_tokens,
            "total_cost_usd": round(total_cost, 2),
            "avg_execution_time_ms": int(sum(elapsed_values) / max(1, len(elapsed_values))) if elapsed_values else 0,
            "active_agents_count": len(AGENT_SPECS),
            "memory_hit_rate": 86.7,
            "pending_approvals": pending_approvals,
            "companies_discovered": sum(len(run.get("companies", [])) for run in self.runs.values()),
        }

    def get_dashboard_snapshot(self) -> dict[str, Any]:
        workflow = self._active_workflow()
        recent_runs = sorted(self.runs.values(), key=lambda item: item["created_at"], reverse=True)
        recent_companies = self._top_companies()
        latest_run = recent_runs[0] if recent_runs else None

        planner_stage = "Execution complete"
        planner_message = "Planner is standing by."
        if latest_run:
            planner_stage = latest_run.get("current_step", planner_stage)
            planner_message = latest_run.get("planner_message", planner_message)

        metrics = self.get_analytics_summary()
        workflow_status = {
            "live_runs": sum(1 for run in self.runs.values() if run["status"] == "running"),
            "paused_runs": sum(1 for run in self.runs.values() if run["status"] == "paused"),
            "completed_today": metrics["successful_runs"],
            "pending_approvals": metrics["pending_approvals"],
        }

        chart_points = [
            {"label": "Mon", "value": 24},
            {"label": "Tue", "value": 32},
            {"label": "Wed", "value": 29},
            {"label": "Thu", "value": 45},
            {"label": "Fri", "value": 52},
            {"label": "Sat", "value": 60},
            {"label": "Sun", "value": 58},
        ]

        memory_groups: dict[str, list[dict[str, Any]]] = {}
        for entry in self.memory_entries:
            memory_groups.setdefault(entry["memory_type"], []).append(entry)

        api_status = [
            {"label": "FastAPI", "state": "online", "detail": "Demo API responding"},
            {"label": "Redis", "state": "optional", "detail": "Using in-memory fallback"},
            {"label": "PostgreSQL", "state": "ready", "detail": "SQLite demo seed active"},
            {"label": "WebSocket", "state": "live", "detail": "Planner and agent events streaming"},
        ]

        return {
            "metrics": metrics,
            "workflow_status": workflow_status,
            "planner": {
                "stage": planner_stage,
                "message": planner_message,
                "reasoning": latest_run.get("planner_reasoning", []) if latest_run else [
                    "Reading memory and historical workflows.",
                    "Selecting only the agents required for the objective.",
                    "Avoiding duplicate enrichment and redundant searches.",
                ],
            },
            "projects": copy.deepcopy(self.projects),
            "workflows": copy.deepcopy(self.workflows),
            "running_jobs": [self._serialize_run(run) for run in recent_runs[:4]],
            "recent_runs": [self._serialize_run(run) for run in recent_runs[:6]],
            "agents": self.list_agents(),
            "companies": recent_companies,
            "approvals": self.get_approvals(),
            "reports": self.get_reports(),
            "notifications": self.get_notifications(),
            "memory": {
                "total_entries": len(self.memory_entries),
                "groups": memory_groups,
                "entries": self.get_memory_entries(),
            },
            "planner_activity": self.get_planner_activity(),
            "timeline": [
                {"label": "Planning", "status": "complete"},
                {"label": "Discovery", "status": "complete"},
                {"label": "Validation", "status": "complete"},
                {"label": "Enrichment", "status": "complete"},
                {"label": "Approval", "status": "live"},
                {"label": "Reporting", "status": "live"},
            ],
            "chart_points": chart_points,
            "api_status": api_status,
            "command_palette_actions": [
                {"label": "Launch demo workflow", "shortcut": "Enter"},
                {"label": "Create workflow", "shortcut": "Ctrl+N"},
                {"label": "Open reports", "shortcut": "R"},
                {"label": "Toggle memory viewer", "shortcut": "M"},
            ],
            "workflow_graph": workflow["graph_data"],
            "workflow_template": workflow,
            "memory_hit_rate": metrics["memory_hit_rate"],
        }

    async def launch_demo_run(self, workflow_id: str | None = None, input_data: dict[str, Any] | None = None) -> dict[str, Any]:
        async with self.lock:
            workflow = self.get_workflow(workflow_id or self._active_workflow()["id"])
            run_id = str(uuid.uuid4())
            run = {
                "id": run_id,
                "workflow_id": workflow["id"],
                "name": workflow["name"],
                "status": "running",
                "trigger": "demo",
                "input_data": input_data or {"objective": "Discover and qualify enterprise prospects"},
                "output_data": {},
                "planner_reasoning": [],
                "agent_results": {},
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "started_at": _iso(),
                "completed_at": None,
                "created_at": _iso(),
                "elapsed_ms": 0,
                "progress": 0,
                "current_step": "Planner initializing",
                "planner_message": "Planner is analyzing request and reading memory.",
                "companies": [],
                "approvals": [],
                "agent_logs": [],
                "approval_event": asyncio.Event(),
                "approval_result": None,
                "execution_graph": workflow["graph_data"],
            }
            self.runs[run_id] = run
            self.workflows[0]["run_count"] += 1
            self.workflows[0]["last_run_status"] = "running"
            self._record_planner_activity(
                "Planner began a new execution",
                f"Workflow {workflow['name']} launched in demo mode.",
            )
            self._record_notification(
                "approval_required",
                "Demo workflow started",
                "The planner is executing the customer discovery pipeline in real time.",
                {"run_id": run_id, "workflow_id": workflow["id"]},
            )

            task = asyncio.create_task(self._execute_demo_run(run_id))
            self.run_tasks[run_id] = task

        return self.get_run(run_id)

    async def respond_to_approval(self, approval_id: str, decision: str, comment: str | None = None, edited_content: dict[str, Any] | None = None) -> dict[str, Any]:
        async with self.lock:
            if approval_id not in self.approvals:
                raise KeyError(approval_id)

            approval = self.approvals[approval_id]
            approval["status"] = decision
            approval["reviewer_comment"] = comment
            approval["edited_content"] = edited_content
            approval["reviewed_by"] = "demo-user"
            approval["reviewed_at"] = _iso()

            run = self._get_run(approval["run_id"])
            run["approval_result"] = approval
            run["approvals"] = [approval]
            if decision == "rejected":
                run["status"] = "failed"
                run["current_step"] = "Approval rejected"
                run["planner_message"] = "Human reviewer rejected the recommendation."
            else:
                run["status"] = "running"
                run["current_step"] = "Resuming workflow"
                run["planner_message"] = "Human review approved the recommendation. Continuing execution."
            run["approval_event"].set()

        return copy.deepcopy(approval)

    async def _execute_demo_run(self, run_id: str):
        timeline = [
            ("Planner Agent", "Reading shared memory and inspecting the workflow graph.", "Selecting only the agents that add value.", 0.5),
            ("Search Agent", "Scanning market signals and public sources for prospects.", "Found companies with strong growth indicators.", 0.8),
            ("Company Validation Agent", "Filtering out duplicates and low-confidence entities.", "Removed weak candidates and stale records.", 0.6),
            ("ICP Matching Agent", "Scoring companies against the buyer profile.", "Prioritized the highest-fit accounts.", 0.7),
            ("Market Intelligence Agent", "Reading news, funding, and competitive signals.", "Detected expansion and hiring momentum.", 0.7),
            ("Company Enrichment Agent", "Adding firmographics and technology context.", "Built richer account profiles.", 0.7),
            ("Decision Maker Finder", "Locating executive stakeholders.", "Identified buying committee members.", 0.7),
            ("LinkedIn Agent", "Enriching people profiles with social context.", "Validated professional identity matches.", 0.4),
            ("Email Enrichment Agent", "Verifying business email addresses.", "Prepared outreach-ready contact records.", 0.4),
            ("Phone Enrichment Agent", "Resolving direct dial numbers.", "Added phone intelligence where available.", 0.35),
            ("Summary Agent", "Writing executive summaries for each account.", "Compressed findings into concise narratives.", 0.5),
            ("Recommendation Agent", "Ranking next-best actions.", "Prepared a human review recommendation.", 0.6),
        ]

        try:
            for index, (agent_name, planner_message, log_message, pause_seconds) in enumerate(timeline, start=1):
                async with self.lock:
                    run = self._get_run(run_id)
                    run["current_step"] = agent_name
                    run["planner_message"] = planner_message
                    run["progress"] = min(72, index * 6)
                    run["planner_reasoning"].append(planner_message)
                    run["agent_logs"].append(
                        {
                            "agent_name": agent_name,
                            "status": "running",
                            "message": log_message,
                            "created_at": _iso(),
                        }
                    )

                await ws_manager.send_planner_step(run_id, _slug(agent_name), planner_message)
                await ws_manager.send_agent_event(run_id, _slug(agent_name), agent_name, "progress", progress=35, message=planner_message)
                await asyncio.sleep(pause_seconds)

            top_companies = self._top_companies()
            approval_payload = {
                "title": "Approve prospect shortlist",
                "content": {
                    "headline": "Three accounts are ready for human review",
                    "summary": "The planner produced a shortlist with contact intelligence and a recommended outreach plan.",
                    "companies": top_companies[:3],
                },
            }
            approval_id = str(uuid.uuid4())

            async with self.lock:
                run = self._get_run(run_id)
                approval = {
                    "id": approval_id,
                    "run_id": run_id,
                    "agent_id": "human_approval_agent",
                    "title": approval_payload["title"],
                    "content": approval_payload["content"],
                    "status": "pending",
                    "reviewer_comment": None,
                    "edited_content": None,
                    "reviewed_by": None,
                    "reviewed_at": None,
                    "created_at": _iso(),
                }
                self.approvals[approval_id] = approval
                run["status"] = "paused"
                run["current_step"] = "Human Approval Agent"
                run["planner_message"] = "Human review required before the recommendation can be finalized."
                run["progress"] = 78
                run["approvals"] = [approval]
                self._record_notification(
                    "approval_required",
                    "Approval required",
                    "The shortlist is ready for review, edit, or rejection.",
                    {"run_id": run_id, "approval_id": approval_id},
                )

            await ws_manager.send_approval_required(run_id, approval_id, approval_payload)
            asyncio.create_task(self._auto_approve_demo(run_id, approval_id))
            await self._get_run(run_id)["approval_event"].wait()

            async with self.lock:
                run = self._get_run(run_id)
                approval = run.get("approval_result")
                if approval and approval.get("status") == "rejected":
                    run["status"] = "failed"
                    run["completed_at"] = _iso()
                    run["elapsed_ms"] = 0
                    run["planner_message"] = "Workflow stopped after a human rejection."
                    run["current_step"] = "Human review complete"
                    self.workflows[0]["last_run_status"] = "failed"
                    self._record_notification(
                        "workflow_failed",
                        "Workflow paused",
                        "The human reviewer rejected the recommendation.",
                        {"run_id": run_id},
                    )
                    return

                run["status"] = "running"
                run["current_step"] = "Report Generator"
                run["planner_message"] = "Approval received. Generating report and writing memory."
                run["progress"] = 88

            await ws_manager.send_planner_step(run_id, "reporting", "Generating a shareable report and persisting the execution memory.")
            await ws_manager.send_agent_event(run_id, "report_generator", "Report Generator", "progress", progress=45, message="Rendering markdown, CSV, and PDF-friendly report payloads.")
            await asyncio.sleep(0.8)

            report_id = str(uuid.uuid4())
            report = {
                "id": report_id,
                "run_id": run_id,
                "title": "B2B Customer Discovery Report",
                "format": "markdown",
                "file_path": f"/reports/{report_id}.md",
                "shareable_url": f"/share/{report_id}",
                "created_at": _iso(),
            }
            memory_entries = [
                {
                    "id": str(uuid.uuid4()),
                    "key": f"workflow.{run_id}.summary",
                    "value": {"companies": top_companies[:5], "decision": "approved"},
                    "memory_type": "workflow",
                    "source_run_id": run_id,
                    "ttl_seconds": None,
                    "access_count": 1,
                    "last_accessed": _iso(),
                    "created_at": _iso(),
                },
                {
                    "id": str(uuid.uuid4()),
                    "key": f"planner.{run_id}.decision",
                    "value": {"selected_agents": [spec.id for spec in AGENT_SPECS]},
                    "memory_type": "planner",
                    "source_run_id": run_id,
                    "ttl_seconds": None,
                    "access_count": 1,
                    "last_accessed": _iso(),
                    "created_at": _iso(),
                },
            ]

            async with self.lock:
                run = self._get_run(run_id)
                run["companies"] = top_companies
                run["output_data"] = {
                    "summary": "Demo workflow completed with approved shortlist and shareable report.",
                    "companies": top_companies,
                    "report": report,
                }
                run["total_tokens"] = sum(spec.avg_token_usage for spec in AGENT_SPECS)
                run["total_cost_usd"] = round(run["total_tokens"] * 0.000018, 2)
                run["status"] = "completed"
                run["progress"] = 100
                run["current_step"] = "Execution complete"
                run["planner_message"] = "Execution complete. The report is ready for export and sharing."
                run["completed_at"] = _iso()
                run["elapsed_ms"] = 20480
                run["agent_logs"].append(
                    {
                        "agent_name": "Report Generator",
                        "status": "completed",
                        "message": "Final report generated successfully.",
                        "created_at": _iso(),
                    }
                )
                run["agent_logs"].append(
                    {
                        "agent_name": "Memory Agent",
                        "status": "completed",
                        "message": "Execution memory persisted for future runs.",
                        "created_at": _iso(),
                    }
                )
                run["agent_logs"].append(
                    {
                        "agent_name": "Analytics Agent",
                        "status": "completed",
                        "message": "Metrics captured and summarized.",
                        "created_at": _iso(),
                    }
                )
                run["reports"] = [report]
                self.reports.insert(0, report)
                self.memory_entries[0:0] = memory_entries
                self.workflows[0]["last_run_status"] = "completed"
                self.workflows[0]["updated_at"] = _iso()

            self._record_planner_activity(
                "Planner completed execution",
                "Shared memory, approvals, reports, and analytics were updated.",
            )
            self._record_notification(
                "workflow_completed",
                "Workflow completed",
                "The report is ready and the shortlist has been approved.",
                {"run_id": run_id, "report_id": report_id},
            )
            await ws_manager.send_agent_event(run_id, "analytics_agent", "Analytics Agent", "completed", progress=100, message="Analytics captured for the completed run.")
            await ws_manager.send_workflow_completed(run_id, {"run_id": run_id, "report_id": report_id, "status": "completed"})
        finally:
            self.run_tasks.pop(run_id, None)

    async def _auto_approve_demo(self, run_id: str, approval_id: str):
        await asyncio.sleep(1.4)
        async with self.lock:
            approval = self.approvals.get(approval_id)
            if not approval or approval.get("status") != "pending":
                return

        await self.respond_to_approval(
            approval_id,
            "approved",
            comment="Auto-approved by demo mode to complete the one-click walkthrough.",
        )


runtime = DemoRuntime()