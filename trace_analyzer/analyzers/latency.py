from trace_analyzer.analyzers.base import Analyzer
from trace_analyzer.schema.report import (
    Finding,
    FindingCategory,
    Severity,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
)


class LatencyAnalyzer(Analyzer):
    """
    Detects slow execution steps.
    """

    WARNING_THRESHOLD_MS = 2000
    CRITICAL_THRESHOLD_MS = 5000

    def analyze(
        self,
        trace: NormalizedTrace,
    ) -> list[Finding]:

        findings: list[Finding] = []

        for step in trace.steps:

            if step.latency_ms is None:
                continue

            if (
                step.latency_ms
                < self.WARNING_THRESHOLD_MS
            ):
                continue

            severity = (
                Severity.CRITICAL
                if (
                    step.latency_ms
                    >= self.CRITICAL_THRESHOLD_MS
                )
                else Severity.WARNING
            )

            findings.append(
                Finding(
                    finding_id=(
                        f"latency-{step.step_id}"
                    ),
                    severity=severity,
                    category=FindingCategory.LATENCY,
                    title=(
                        "Slow execution step detected"
                    ),
                    description=(
                        f"Step '{step.step_id}' "
                        f"took {step.latency_ms} ms."
                    ),
                    affected_steps=[
                        step.step_id
                    ],
                    latency_impact_ms=(
                        step.latency_ms
                    ),
                    recommendation=(
                        "Reduce latency through "
                        "caching, batching, or "
                        "parallel execution."
                    ),
                    evidence=(
                        f"Latency: "
                        f"{step.latency_ms} ms"
                    ),
                    metadata={
                        "latency_ms": (
                            step.latency_ms
                        )
                    },
                )
            )

        return findings