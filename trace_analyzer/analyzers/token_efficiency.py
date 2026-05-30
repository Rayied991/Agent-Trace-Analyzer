from trace_analyzer.analyzers.base import Analyzer
from trace_analyzer.schema.report import (
    Finding,
    FindingCategory,
    Severity,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
)


class TokenEfficiencyAnalyzer(Analyzer):
    """
    Detects inefficient token usage
    within agent execution traces.
    """

    # -----------------------------------------
    # Thresholds
    # -----------------------------------------

    LARGE_INPUT_THRESHOLD = 4000
    LARGE_OUTPUT_THRESHOLD = 2000

    CRITICAL_INPUT_THRESHOLD = 10000
    CRITICAL_OUTPUT_THRESHOLD = 5000

    def analyze(
        self,
        trace: NormalizedTrace,
    ) -> list[Finding]:
        """
        Analyze trace for inefficient
        token usage patterns.
        """

        findings: list[Finding] = []

        # -----------------------------------------
        # Iterate Through Steps
        # -----------------------------------------

        for step in trace.steps:

            # -----------------------------------------
            # Large Input Detection
            # -----------------------------------------

            if (
                step.input_tokens
                > self.LARGE_INPUT_THRESHOLD
            ):

                severity = (
                    Severity.CRITICAL
                    if (
                        step.input_tokens
                        > self.CRITICAL_INPUT_THRESHOLD
                    )
                    else Severity.WARNING
                )

                finding = Finding(
                    finding_id=(
                        f"large-input-{step.step_id}"
                    ),
                    severity=severity,
                    category=FindingCategory.EFFICIENCY,
                    title="Large prompt detected",
                    description=(
                        f"Step '{step.step_id}' "
                        f"consumed "
                        f"{step.input_tokens} input tokens."
                    ),
                    affected_steps=[
                        step.step_id
                    ],
                    token_impact=step.input_tokens,
                    recommendation=(
                        "Compress retrieval context "
                        "or summarize conversation history."
                    ),
                    evidence=(
                        f"Input tokens: "
                        f"{step.input_tokens}"
                    ),
                    metadata={
                        "threshold": (
                            self.LARGE_INPUT_THRESHOLD
                        ),
                        "actual_tokens": (
                            step.input_tokens
                        ),
                    },
                )

                findings.append(finding)

            # -----------------------------------------
            # Large Output Detection
            # -----------------------------------------

            if (
                step.output_tokens
                > self.LARGE_OUTPUT_THRESHOLD
            ):

                severity = (
                    Severity.CRITICAL
                    if (
                        step.output_tokens
                        > self.CRITICAL_OUTPUT_THRESHOLD
                    )
                    else Severity.WARNING
                )

                finding = Finding(
                    finding_id=(
                        f"large-output-{step.step_id}"
                    ),
                    severity=severity,
                    category=FindingCategory.EFFICIENCY,
                    title="Large output detected",
                    description=(
                        f"Step '{step.step_id}' "
                        f"generated "
                        f"{step.output_tokens} output tokens."
                    ),
                    affected_steps=[
                        step.step_id
                    ],
                    token_impact=step.output_tokens,
                    recommendation=(
                        "Reduce verbose reasoning "
                        "or shorten generation length."
                    ),
                    evidence=(
                        f"Output tokens: "
                        f"{step.output_tokens}"
                    ),
                    metadata={
                        "threshold": (
                            self.LARGE_OUTPUT_THRESHOLD
                        ),
                        "actual_tokens": (
                            step.output_tokens
                        ),
                    },
                )

                findings.append(finding)

        return findings