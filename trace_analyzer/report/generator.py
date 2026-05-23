from collections import Counter

from trace_analyzer.schema.report import (
    AuditReport,
    Finding,
    ReportSummary,
    Severity,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
)


class ReportGenerator:
    """
    Generates structured audit reports
    from analyzer findings.
    """

    def generate(
        self,
        trace: NormalizedTrace,
        findings: list[Finding],
    ) -> AuditReport:
        """
        Generate a complete audit report.
        """

        # -----------------------------------------
        # Severity Counts
        # -----------------------------------------

        severity_counts = Counter(
            finding.severity
            for finding in findings
        )

        # -----------------------------------------
        # Aggregate Metrics
        # -----------------------------------------

        wasted_tokens = sum(
            finding.token_impact or 0
            for finding in findings
        )

        total_cost_usd = trace.total_cost_usd

        projected_savings_usd = (
            (wasted_tokens / trace.total_tokens)
            * total_cost_usd
            if trace.total_tokens > 0
            else 0.0
        )

        waste_percentage = (
            (wasted_tokens / trace.total_tokens) * 100
            if trace.total_tokens > 0
            else 0.0
        )

        average_latency_ms = None

        latencies = [
            step.latency_ms
            for step in trace.steps
            if step.latency_ms is not None
        ]

        if latencies:
            average_latency_ms = (
                sum(latencies) / len(latencies)
            )

        # -----------------------------------------
        # Top Issue
        # -----------------------------------------

        top_issue = None

        if findings:
            top_issue = max(
                    findings,
                    key=lambda f: (
                        f.token_impact or 0
                    ),
                ).title

        # -----------------------------------------
        # Build Summary
        # -----------------------------------------

        summary = ReportSummary(
            total_steps=trace.total_steps,
            total_findings=len(findings),
            critical_count=severity_counts.get(
                Severity.CRITICAL,
                0,
            ),
            warning_count=severity_counts.get(
                Severity.WARNING,
                0,
            ),
            info_count=severity_counts.get(
                Severity.INFO,
                0,
            ),
            total_tokens=trace.total_tokens,
            wasted_tokens=wasted_tokens,
            waste_percentage=round(
                waste_percentage,
                2,
            ),
            total_cost_usd=round(
                total_cost_usd,
                6,
            ),
            projected_savings_usd=round(
                projected_savings_usd,
                6,
            ),
            average_latency_ms=(
                round(average_latency_ms, 2)
                if average_latency_ms is not None
                else None
            ),
            top_issue=top_issue,
        )

        # -----------------------------------------
        # Build Audit Report
        # -----------------------------------------

        report = AuditReport(
            report_id=f"audit-{trace.trace_id}",
            trace_id=trace.trace_id,
            findings=findings,
            summary=summary,
            analyzer_version="0.1.0",
            generated_by="Agent Trace Analyzer",
        )

        return report