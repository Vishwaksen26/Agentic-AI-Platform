"""
AgentForge AI – Base Agent Abstract Class

All agents must extend BaseAgent. This ensures:
- Consistent interface
- Built-in logging
- WebSocket event streaming
- Token tracking
- Error handling
- Retry logic
"""

import asyncio
import logging
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional

from backend.core.websocket_manager import ws_manager

logger = logging.getLogger(__name__)


class AgentResult:
    """Standardized output from any agent execution."""

    def __init__(
        self,
        agent_id: str,
        agent_name: str,
        success: bool,
        output: Any = None,
        error: Optional[str] = None,
        token_usage: int = 0,
        elapsed_ms: int = 0,
        metadata: Optional[dict] = None,
    ):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.success = success
        self.output = output
        self.error = error
        self.token_usage = token_usage
        self.elapsed_ms = elapsed_ms
        self.metadata = metadata or {}

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "token_usage": self.token_usage,
            "elapsed_ms": self.elapsed_ms,
            "metadata": self.metadata,
        }


class BaseAgent(ABC):
    """
    Abstract base class for all AgentForge agents.

    Subclasses must implement:
    - agent_id: str  (unique identifier e.g. "search_agent")
    - agent_name: str  (human-readable e.g. "Search Agent")
    - description: str
    - capabilities: list[str]
    - _execute(): core logic

    Subclasses may override:
    - max_retries: int
    - retry_delay_seconds: float
    - category: str
    - icon: str
    - color: str
    """

    # Must be defined by subclass
    agent_id: str = ""
    agent_name: str = ""
    description: str = ""
    capabilities: list[str] = []
    category: str = "general"
    icon: str = "bot"
    color: str = "#6366f1"

    # Runtime configuration
    max_retries: int = 2
    retry_delay_seconds: float = 1.0

    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self._execution_id: str = ""

    async def run(
        self,
        run_id: str,
        input_data: dict,
        shared_memory: dict,
        stream: bool = True,
    ) -> AgentResult:
        """
        Public entry point. Handles streaming, retries, timing, error handling.
        Do NOT override this — override _execute() instead.
        """
        self._execution_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        attempt = 0

        logger.info(f"[{self.agent_name}] Starting (run_id={run_id})")

        if stream:
            await ws_manager.send_agent_event(
                run_id, self.agent_id, self.agent_name, "started",
                progress=0, message=f"{self.agent_name} initializing..."
            )

        while attempt <= self.max_retries:
            try:
                result = await self._execute(run_id, input_data, shared_memory, stream)
                elapsed_ms = int((time.time() - start_time) * 1000)
                result.elapsed_ms = elapsed_ms

                if stream:
                    await ws_manager.send_agent_event(
                        run_id, self.agent_id, self.agent_name, "completed",
                        progress=100,
                        message=f"{self.agent_name} completed successfully",
                        output=result.output if isinstance(result.output, (dict, list, str)) else str(result.output),
                        token_usage=result.token_usage,
                        elapsed_ms=elapsed_ms,
                    )

                logger.info(f"[{self.agent_name}] Completed in {elapsed_ms}ms, tokens={result.token_usage}")
                return result

            except Exception as e:
                attempt += 1
                elapsed_ms = int((time.time() - start_time) * 1000)

                if attempt <= self.max_retries:
                    logger.warning(f"[{self.agent_name}] Attempt {attempt} failed: {e}. Retrying...")
                    if stream:
                        await ws_manager.send_agent_event(
                            run_id, self.agent_id, self.agent_name, "progress",
                            progress=0,
                            message=f"Retry {attempt}/{self.max_retries}: {str(e)[:100]}",
                        )
                    await asyncio.sleep(self.retry_delay_seconds * attempt)
                else:
                    logger.error(f"[{self.agent_name}] All retries exhausted: {e}")
                    if stream:
                        await ws_manager.send_agent_event(
                            run_id, self.agent_id, self.agent_name, "failed",
                            progress=0,
                            message=f"Failed: {str(e)[:200]}",
                            elapsed_ms=elapsed_ms,
                        )
                    return AgentResult(
                        agent_id=self.agent_id,
                        agent_name=self.agent_name,
                        success=False,
                        error=str(e),
                        elapsed_ms=elapsed_ms,
                    )

        # Should never reach here, but safety fallback
        return AgentResult(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            success=False,
            error="Unknown error",
        )

    async def update_progress(self, run_id: str, progress: int, message: str):
        """Helper for subclasses to stream progress updates."""
        await ws_manager.send_agent_event(
            run_id, self.agent_id, self.agent_name, "progress",
            progress=progress, message=message
        )

    @abstractmethod
    async def _execute(
        self,
        run_id: str,
        input_data: dict,
        shared_memory: dict,
        stream: bool,
    ) -> AgentResult:
        """Core agent logic. Must be implemented by all subclasses."""
        ...

    def to_info_dict(self) -> dict:
        """Return agent metadata for the agent registry API."""
        return {
            "id": self.agent_id,
            "name": self.agent_name,
            "description": self.description,
            "category": self.category,
            "capabilities": self.capabilities,
            "icon": self.icon,
            "color": self.color,
            "max_retries": self.max_retries,
        }
