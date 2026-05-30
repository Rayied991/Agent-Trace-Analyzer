from pathlib import Path

from trace_analyzer.schema.report import (
    AuditReport,
)


class HTMLReportExporter:
    """
    Exports audit reports
    as standalone HTML files.
    """

    def export(
        self,
        report: AuditReport,
        output_path: str,
    ) -> None:
        """
        Export report to HTML.
        """

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<title>Agent Trace Audit Report</title>

<style>

body {{
    font-family: Arial, sans-serif;
    margin: 40px;
}}

h1 {{
    color: #2c3e50;
}}

h2 {{
    margin-top: 30px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th,
td {{
    border: 1px solid #ddd;
    padding: 10px;
}}

th {{
    background-color: #f5f5f5;
}}

.warning {{
    color: orange;
    font-weight: bold;
}}

.critical {{
    color: red;
    font-weight: bold;
}}

.info {{
    color: blue;
    font-weight: bold;
}}

.summary-box {{
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
}}

</style>
</head>

<body>

<h1>Agent Trace Audit Report</h1>

<div class="summary-box">

<p>
<b>Trace ID:</b>
{report.trace_id}
</p>

<p>
<b>Total Findings:</b>
{report.summary.total_findings}
</p>

<p>
<b>Total Tokens:</b>
{report.summary.total_tokens}
</p>

<p>
<b>Wasted Tokens:</b>
{report.summary.wasted_tokens}
</p>

<p>
<b>Reliability Score:</b>
{report.summary.reliability_score}/100
</p>

<p>
<b>Top Issue:</b>
{report.summary.top_issue}
</p>

</div>

<h2>Findings</h2>

<table>

<tr>
<th>Severity</th>
<th>Category</th>
<th>Title</th>
<th>Impact</th>
<th>Recommendation</th>
</tr>

"""

        for finding in report.findings:

            if finding.token_impact is not None:

                impact = (
                    f"{finding.token_impact} tokens"
                )

            elif (
                finding.reliability_impact
                is not None
            ):

                impact = (
                    f"-{finding.reliability_impact} reliability"
                )

            elif (
                finding.latency_impact_ms
                is not None
            ):

                impact = (
                    f"{finding.latency_impact_ms:.0f} ms"
                )

            else:

                impact = "-"

            html += f"""
<tr>
<td class="{finding.severity.value}">
{finding.severity.value.upper()}
</td>

<td>
{finding.category.value}
</td>

<td>
{finding.title}
</td>

<td>
{impact}
</td>

<td>
{finding.recommendation or "-"}
</td>

</tr>
"""

        html += """
</table>

</body>
</html>
"""

        Path(output_path).write_text(
            html,
            encoding="utf-8",
        )