from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
)

from trace_analyzer.schema.report import (
    AuditReport,
)


class PDFReportExporter:

    def export(
        self,
        report: AuditReport,
        output_path: str,
    ) -> None:

        doc = SimpleDocTemplate(output_path)
        styles = getSampleStyleSheet()
        content = []

        # ── Title ──────────────────────────────
        content.append(
            Paragraph(
                "Agent Trace Audit Report",
                styles["Title"],
            )
        )
        content.append(Spacer(1, 12))
        content.append(
            Paragraph(
                f"Trace ID: {report.trace_id}",
                styles["BodyText"],
            )
        )
        content.append(Spacer(1, 20))

        # ── Executive Summary ──────────────────
        content.append(
            Paragraph("Executive Summary", styles["Heading1"])
        )
        content.append(
            Paragraph(
                f"Reliability Score: {report.summary.reliability_score}",
                styles["BodyText"],
            )
        )
        content.append(
            Paragraph(
                f"Total Tokens: {report.summary.total_tokens}",
                styles["BodyText"],
            )
        )
        content.append(
            Paragraph(
                f"Total Findings: {report.summary.total_findings}",  # improvement 1
                styles["BodyText"],
            )
        )
        content.append(
            Paragraph(
                f"Waste Percentage: {report.summary.waste_percentage}%",
                styles["BodyText"],
            )
        )
        content.append(
            Paragraph(
                f"Execution Cost: ${report.summary.total_cost_usd}",  # improvement 2
                styles["BodyText"],
            )
        )
        content.append(
            Paragraph(
                f"Estimated Savings: ${report.summary.projected_savings_usd}",
                styles["BodyText"],
            )
        )
        content.append(Spacer(1, 20))

        # ── Analyzer Breakdown ─────────────────
        content.append(
            Paragraph("Analyzer Breakdown", styles["Heading1"])
        )
        for item in report.analyzer_breakdown:
            content.append(
                Paragraph(
                    f"{item.analyzer}: {item.findings}",
                    styles["BodyText"],
                )
            )
        content.append(Spacer(1, 20))

        # ── Severity Breakdown ─────────────────
        content.append(
            Paragraph("Severity Breakdown", styles["Heading1"])
        )
        content.append(
            Paragraph(
                f"Critical: {report.summary.critical_count}",
                styles["BodyText"],
            )
        )
        content.append(
            Paragraph(
                f"Warning: {report.summary.warning_count}",
                styles["BodyText"],
            )
        )
        content.append(
            Paragraph(
                f"Info: {report.summary.info_count}",
                styles["BodyText"],
            )
        )
        content.append(Spacer(1, 20))

        # ── Findings ───────────────────────────
        content.append(PageBreak())
        content.append(
            Paragraph("Findings", styles["Heading1"])
        )
        for finding in report.findings:
            content.append(
                Paragraph(
                    f"[{finding.severity.upper()}] {finding.title}",  # improvement 3
                    styles["Heading2"],
                )
            )
            content.append(
                Paragraph(finding.description, styles["BodyText"])
            )
            if finding.token_impact:                                   # improvement 4
                content.append(
                    Paragraph(
                        f"Token Impact: {finding.token_impact}",
                        styles["BodyText"],
                    )
                )
            if finding.latency_impact_ms:
                content.append(
                    Paragraph(
                        f"Latency Impact: {finding.latency_impact_ms} ms",
                        styles["BodyText"],
                    )
                )
            if finding.reliability_impact:
                content.append(
                    Paragraph(
                        f"Reliability Impact: {finding.reliability_impact}",
                        styles["BodyText"],
                    )
                )
            if finding.recommendation:
                content.append(
                    Paragraph(finding.recommendation, styles["BodyText"])
                )
            content.append(Spacer(1, 12))

        # ── Recommendations ────────────────────
        content.append(PageBreak())
        content.append(
            Paragraph("Recommendations", styles["Heading1"])
        )
        for finding in report.findings:
            if finding.recommendation:
                content.append(
                    Paragraph(
                        f"• {finding.recommendation}",
                        styles["BodyText"],
                    )
                )
        content.append(Spacer(1, 20))

        # ── Metadata ───────────────────────────
        content.append(PageBreak())                                    # improvement 5
        content.append(
            Paragraph("Report Generated By", styles["Heading1"])
        )
        content.append(
            Paragraph(
                report.generated_by,
                styles["BodyText"],
            )
        )
        content.append(
            Paragraph(
                f"Analyzer Version: {report.analyzer_version}",
                styles["BodyText"],
            )
        )

        doc.build(content)