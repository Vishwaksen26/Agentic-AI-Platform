"""AgentForge AI Backend – WebSocket Connection Manager"""

import json
import logging
from collections import defaultdict
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections per workflow run."""

    def __init__(self):
        # run_id -> list of WebSocket connections
        self.connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, websocket: WebSocket, run_id: str):
        await websocket.accept()
        self.connections[run_id].append(websocket)
        logger.info(f"WS connected: run_id={run_id}, total={len(self.connections[run_id])}")

    def disconnect(self, websocket: WebSocket, run_id: str):
        if run_id in self.connections:
            self.connections[run_id].remove(websocket)
            if not self.connections[run_id]:
                del self.connections[run_id]
        logger.info(f"WS disconnected: run_id={run_id}")

    async def broadcast(self, run_id: str, event: dict[str, Any]):
        """Send event to all subscribers of a run."""
        dead: list[WebSocket] = []
        for ws in self.connections.get(run_id, []):
            try:
                await ws.send_text(json.dumps(event))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.connections[run_id].remove(ws)

    async def broadcast_all(self, event: dict[str, Any]):
        """Send event to ALL connected clients (system-wide notifications)."""
        for run_id in list(self.connections.keys()):
            await self.broadcast(run_id, event)

    async def send_planner_step(self, run_id: str, step: str, detail: str = ""):
        await self.broadcast(run_id, {
            "type": "planner_thinking",
            "step": step,
            "detail": detail,
        })

    async def send_agent_event(
        self,
        run_id: str,
        agent_id: str,
        agent_name: str,
        event_type: str,  # started|progress|completed|failed|skipped
        progress: int = 0,
        message: str = "",
        output: Any = None,
        token_usage: int = 0,
        elapsed_ms: int = 0,
    ):
        await self.broadcast(run_id, {
            "type": f"agent_{event_type}",
            "agent_id": agent_id,
            "agent_name": agent_name,
            "progress": progress,
            "message": message,
            "output": output,
            "token_usage": token_usage,
            "elapsed_ms": elapsed_ms,
        })

    async def send_approval_required(self, run_id: str, approval_id: str, data: dict):
        await self.broadcast(run_id, {
            "type": "approval_required",
            "approval_id": approval_id,
            "data": data,
        })

    async def send_workflow_completed(self, run_id: str, summary: dict):
        await self.broadcast(run_id, {
            "type": "workflow_completed",
            "summary": summary,
        })


# Singleton
ws_manager = WebSocketManager()
