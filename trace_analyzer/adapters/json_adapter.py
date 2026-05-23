from typing import Any

from trace_analyzer.adapters.base import TraceAdapter
from trace_analyzer.schema.trace import (
    NormalizedTrace,
    StepType,
    TraceStep,
)


class JSONTraceAdapter(TraceAdapter):
    """
    Adapter for generic JSON trace files.
    """

    def can_handle(self, raw_trace: Any) -> bool:
        """
        Check whether trace appears
        to follow expected JSON structure.
        """

        return (
    isinstance(raw_trace, dict)
    and isinstance(raw_trace.get("steps"), list)
)

    def parse(self, raw_trace: Any) -> NormalizedTrace:
        """
        Convert raw JSON trace into NormalizedTrace.
        """

        if not self.can_handle(raw_trace):
            raise ValueError(
                "Unsupported trace format for JSONTraceAdapter"
            )

        normalized_trace = NormalizedTrace(
            trace_id=raw_trace.get("trace_id", "unknown-trace"),
            agent_name=raw_trace.get("agent_name"),
            source_format="json",
            raw_trace=raw_trace,
        )

        for step_data in raw_trace.get("steps", []):
           try:
                step = TraceStep(
                    step_id=step_data["step_id"],
                    step_type=StepType(step_data["step_type"]),
                    content=step_data.get("content", ""),
                    tool_name=step_data.get("tool_name"),
                    tool_args=step_data.get("tool_args"),
                    tool_result=step_data.get("tool_result"),
                    input_tokens=step_data.get("input_tokens", 0),
                    output_tokens=step_data.get("output_tokens", 0),
                    latency_ms=step_data.get("latency_ms"),
                    model=step_data.get("model"),
                    metadata=step_data.get("metadata", {}),
                )

                normalized_trace.add_step(step)
                
           except Exception as e:
                raise ValueError(
                    f"Failed to parse trace step: {step_data}"
                ) from e     

        return normalized_trace