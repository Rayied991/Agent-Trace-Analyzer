from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# =========================================================
# Step Types
# =========================================================

class StepType(str, Enum):
    """
    Represents the type of execution step
    inside an agent workflow trace.
    """

    LLM_CALL = "llm_call"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    REASONING = "reasoning"
    SYSTEM = "system"
    MEMORY = "memory"
    RETRY = "retry"


# =========================================================
# Trace Step
# =========================================================

class TraceStep(BaseModel):
    """
    Represents a single execution step
    inside an agent trace.

    Examples:
    - LLM request
    - Tool invocation
    - Tool result
    - Reasoning step
    - Retry
    """

    # -----------------------------
    # Core Identity
    # -----------------------------
    step_id: str = Field(
        ...,
        description="Unique identifier for this step"
    )

    step_type: StepType = Field(
        ...,
        description="Type of execution step"
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the step occurred"
    )

    # -----------------------------
    # Content
    # -----------------------------
    content: str = Field(
        ...,
        description="Raw textual content of the step"
    )

    # -----------------------------
    # Tool Metadata
    # -----------------------------
    tool_name: Optional[str] = Field(
        default=None,
        description="Name of tool used in this step"
    )

    tool_args: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Arguments passed to the tool"
    )

    tool_result: Optional[str] = Field(
        default=None,
        description="Result returned by the tool"
    )

    # -----------------------------
    # Token Metrics
    # -----------------------------
    input_tokens: int = Field(
        default=0,
        ge=0,
        description="Input token count"
    )

    output_tokens: int = Field(
        default=0,
        ge=0,
        description="Output token count"
    )

    # -----------------------------
    # Performance Metrics
    # -----------------------------
    latency_ms: Optional[float] = Field(
        default=None,
        ge=0,
        description="Latency in milliseconds"
    )

    # -----------------------------
    # Model Metadata
    # -----------------------------
    model: Optional[str] = Field(
        default=None,
        description="LLM model used"
    )

    # -----------------------------
    # Additional Metadata
    # -----------------------------
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the step"
    )

    model_config = {
        "extra": "allow",
        "validate_assignment": True
    }


# =========================================================
# Normalized Trace
# =========================================================

class NormalizedTrace(BaseModel):
    """
    Unified internal representation
    of an entire agent execution trace.

    Every framework adapter converts
    raw traces into this format.
    """

    # -----------------------------
    # Trace Identity
    # -----------------------------
    trace_id: str = Field(
        ...,
        description="Unique trace identifier"
    )

    agent_name: Optional[str] = Field(
        default=None,
        description="Name of the agent/system"
    )

    created_at: datetime = Field(
       default_factory=lambda: datetime.now(timezone.utc),
        description="Trace creation timestamp"
    )

    # -----------------------------
    # Execution Steps
    # -----------------------------
    steps: List[TraceStep] = Field(
        default_factory=list,
        description="List of execution steps"
    )

    # -----------------------------
    # Aggregate Metrics
    # -----------------------------
    total_input_tokens: int = Field(
        default=0,
        ge=0,
        description="Total input tokens"
    )

    total_output_tokens: int = Field(
        default=0,
        ge=0,
        description="Total output tokens"
    )

    total_cost_usd: float = Field(
        default=0.0,
        ge=0,
        description="Total estimated cost in USD"
    )

    # -----------------------------
    # Source Metadata
    # -----------------------------
    source_format: Optional[str] = Field(
        default=None,
        description="Original source format (OpenAI, LangGraph, etc.)"
    )

    raw_trace: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Original raw trace payload"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional trace-level metadata"
    )

    model_config = {
        "extra": "allow",
        "validate_assignment": True
    }

    # =====================================================
    # Helper Properties
    # =====================================================

    @property
    def total_tokens(self) -> int:
        """
        Returns total tokens used in the trace.
        """
        return self.total_input_tokens + self.total_output_tokens

    @property
    def total_steps(self) -> int:
        """
        Returns total number of execution steps.
        """
        return len(self.steps)

    # =====================================================
    # Helper Methods
    # =====================================================

    def add_step(self, step: TraceStep) -> None:
        """
        Add a new step to the trace
        and update aggregate metrics.
        """

        self.steps.append(step)

        self.total_input_tokens += step.input_tokens
        self.total_output_tokens += step.output_tokens

    def get_steps_by_type(
        self,
        step_type: StepType
    ) -> List[TraceStep]:
        """
        Retrieve all steps of a given type.
        """

        return [
            step
            for step in self.steps
            if step.step_type == step_type
        ]