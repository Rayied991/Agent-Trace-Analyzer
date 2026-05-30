from trace_analyzer.analyzers.base import Analyzer
from trace_analyzer.schema.report import (
    Finding,
    FindingCategory,
    Severity,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
    StepType,
)


class ReasoningAnalyzer(Analyzer):
    """
    Detects unsupported conclusions
    and basic reasoning gaps.

    MVP Version:
    - looks for conclusion phrases
    - checks whether prior tool evidence exists
    """

    CONCLUSION_PHRASES = [
        "therefore",
        "thus",
        "we can conclude",
        "the answer is",
        "this means",
    ]

    def analyze(
        self,
        trace: NormalizedTrace,
    ) -> list[Finding]:
        """
        Analyze reasoning steps
        for unsupported conclusions.
        """

        findings: list[Finding] = []

        # -----------------------------------------
        # Track available evidence
        # -----------------------------------------

        evidence_seen = False

        # -----------------------------------------
        # Walk through trace
        # -----------------------------------------

        for step in trace.steps:

            # -----------------------------------------
            # Evidence detected
            # -----------------------------------------

            if step.step_type == StepType.TOOL_RESULT:
                evidence_seen = True
                continue

            # -----------------------------------------
            # Only inspect LLM outputs
            # -----------------------------------------

            if step.step_type != StepType.LLM_CALL:
                continue

            content = step.content.lower()

            # -----------------------------------------
            # Check for conclusion phrases
            # -----------------------------------------

            contains_conclusion = any(
                phrase in content
                for phrase in self.CONCLUSION_PHRASES
            )

            if not contains_conclusion:
                continue

            # -----------------------------------------
            # Unsupported conclusion
            # -----------------------------------------

            if not evidence_seen:

                finding = Finding(
                    finding_id=(
                        f"reasoning-gap-{step.step_id}"
                    ),
                    severity=Severity.WARNING,
                    category=(
                        FindingCategory.REASONING_GAP
                    ),
                    title=(
                        "Unsupported conclusion detected"
                    ),
                    description=(
                        f"Step '{step.step_id}' "
                        "contains a conclusion "
                        "without prior supporting evidence."
                    ),
                   affected_steps=[
                    step.step_id
                ],

                token_impact=None,

                reliability_impact=20,

                recommendation=(
                    "Require supporting tool "
                    "results before making "
                    "factual conclusions."
                ),

                evidence=(
                    step.content[:200]
                ),

                metadata={
                    "conclusion_detected": True,
                    "evidence_found": False,
                },
                )

                findings.append(finding)

        return findings