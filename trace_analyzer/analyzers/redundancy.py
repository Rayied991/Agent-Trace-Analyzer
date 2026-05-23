import hashlib
import json
from collections import defaultdict
from typing import Dict

from trace_analyzer.analyzers.base import Analyzer
from trace_analyzer.schema.report import (
    Finding,
    FindingCategory,
    Severity,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
    StepType,
    TraceStep,
)


class RedundancyAnalyzer(Analyzer):
    """
    Detects redundant tool calls
    within an agent execution trace.
    """

    def analyze(
        self,
        trace: NormalizedTrace
    ) -> list[Finding]:
        """
        Analyze the trace for duplicate
        tool calls and redundant executions.
        """

        findings: list[Finding] = []

        # -----------------------------------------
        # Track previously seen tool calls
        # -----------------------------------------

        seen_calls: Dict[str, list[TraceStep]] = defaultdict(list)

        # -----------------------------------------
        # Iterate through execution steps
        # -----------------------------------------

        for step in trace.steps:

            # Only analyze tool calls
            if step.step_type != StepType.TOOL_CALL:
                continue

            # Skip incomplete tool calls
            if not step.tool_name:
                continue

            tool_hash = self._generate_tool_hash(step)

            seen_calls[tool_hash].append(step)

        # -----------------------------------------
        # Generate findings for duplicates
        # -----------------------------------------

        for tool_hash, duplicate_steps in seen_calls.items():

            if len(duplicate_steps) <= 1:
                continue

            first_step = duplicate_steps[0]

            occurrence_count = len(duplicate_steps)

            wasted_input_tokens = sum(
                step.input_tokens
                for step in duplicate_steps[1:]
            )

            wasted_output_tokens = sum(
                step.output_tokens
                for step in duplicate_steps[1:]
            )

            wasted_tokens = (
                wasted_input_tokens
                + wasted_output_tokens
            )

            total_latency_ms = sum(
                step.latency_ms or 0
                for step in duplicate_steps[1:]
            )

            affected_steps = [
                step.step_id
                for step in duplicate_steps
            ]

            severity = (
                Severity.CRITICAL
                if occurrence_count >= 5
                else Severity.WARNING
            )

            finding = Finding(
                finding_id=(
                "redundancy-"
                + hashlib.md5(
                    tool_hash.encode()
                ).hexdigest()[:8]
            ),
               severity=severity,
                category=FindingCategory.REDUNDANCY,
                title="Duplicate tool call detected",
                description=(
                    f"Tool '{first_step.tool_name}' "
                    f"was called {occurrence_count} times "
                    f"with identical arguments."
                ),
                affected_steps=affected_steps,
                token_impact=wasted_tokens,
                latency_impact_ms=total_latency_ms,
                recommendation=(
                    "Consider caching tool results "
                    "or reusing previous outputs."
                ),
                evidence=(
                    f"Duplicate tool call: "
                    f"{first_step.tool_name}"
                ),
                metadata={
                    "tool_name": first_step.tool_name,
                    "tool_args": first_step.tool_args,
                    "occurrences": occurrence_count,
                },
            )

            findings.append(finding)

        return findings

    # =====================================================
    # Helper Methods
    # =====================================================

    def _generate_tool_hash(
        self,
        step: TraceStep
    ) -> str:
        """
        Generate deterministic hash for a tool call.

        Combines:
        - tool name
        - normalized/sorted arguments
        """

        normalized_args = json.dumps(
            step.tool_args or {},
            sort_keys=True,
        )

        return (
            f"{step.tool_name}:{normalized_args}"
        )