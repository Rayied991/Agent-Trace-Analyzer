from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
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

        doc = SimpleDocTemplate(
            output_path
        )

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "Agent Trace Audit Report",
                styles["Title"],
            )
        )

        content.append(
            Spacer(1, 12)
        )

        content.append(
            Paragraph(
                f"Trace ID: {report.trace_id}",
                styles["BodyText"],
            )
        )

        content.append(
            Paragraph(
                f"Reliability Score: {report.summary.reliability_score}",
                styles["BodyText"],
            )
        )

        content.append(
            Paragraph(
                f"Total Findings: {report.summary.total_findings}",
                styles["BodyText"],
            )
        )

        content.append(
            Spacer(1, 20)
        )

        for finding in report.findings:

            content.append(
                Paragraph(
                    finding.title,
                    styles["Heading2"],
                )
            )

            content.append(
                Paragraph(
                    finding.description,
                    styles["BodyText"],
                )
            )

            content.append(
                Paragraph(
                    finding.recommendation
                    or "",
                    styles["BodyText"],
                )
            )

            content.append(
                Spacer(1, 12)
            )

        doc.build(content)