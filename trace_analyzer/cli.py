import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from trace_analyzer.adapters.json_adapter import (
    JSONTraceAdapter,
)
from trace_analyzer.analyzers.redundancy import (
    RedundancyAnalyzer,
)
from trace_analyzer.report.generator import (
    ReportGenerator,
)
from trace_analyzer.schema.report import Severity

app = typer.Typer(
    help="Agent Trace Analyzer CLI"
)

console = Console()


@app.command()
def analyze(
    trace_file: str,
):
    """
    Analyze an agent trace file.
    """

    trace_path = Path(trace_file)

    if not trace_path.exists():

        console.print(
            f"[red]Trace file not found:[/red] {trace_file}"
        )

        raise typer.Exit(code=1)

    # -----------------------------------------
    # Load JSON Trace
    # -----------------------------------------

    with open(
        trace_path,
        "r",
        encoding="utf-8",
    ) as f:

        try:

            raw_trace = json.load(f)

        except json.JSONDecodeError:

            console.print(
                "[red]Invalid JSON trace file.[/red]"
            )

            raise typer.Exit(code=1)

    # -----------------------------------------
    # Parse Trace
    # -----------------------------------------

    adapter = JSONTraceAdapter()

    trace = adapter.parse(raw_trace)

    # -----------------------------------------
    # Run Analyzers
    # -----------------------------------------

    analyzers = [
        RedundancyAnalyzer(),
    ]

    findings: list = []

    for analyzer in analyzers:

        findings.extend(
            analyzer.analyze(trace)
        )

    # -----------------------------------------
    # Generate Report
    # -----------------------------------------

    generator = ReportGenerator()

    report = generator.generate(
        trace=trace,
        findings=findings,
    )

    # -----------------------------------------
    # Render Header
    # -----------------------------------------

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]AGENT TRACE AUDIT REPORT[/bold cyan]",
            border_style="cyan",
        )
    )

    # -----------------------------------------
    # Render Summary Table
    # -----------------------------------------

    summary_table = Table(
        title="Summary"
    )

    summary_table.add_column(
        "Metric",
        style="cyan",
    )

    summary_table.add_column(
        "Value",
        style="green",
    )

    summary_table.add_row(
        "Trace ID",
        report.trace_id,
    )

    summary_table.add_row(
        "Total Steps",
        str(report.summary.total_steps),
    )

    summary_table.add_row(
        "Total Findings",
        str(report.summary.total_findings),
    )

    summary_table.add_row(
        "Total Tokens",
        str(report.summary.total_tokens),
    )

    summary_table.add_row(
        "Wasted Tokens",
        str(report.summary.wasted_tokens),
    )

    summary_table.add_row(
        "Waste Percentage",
        f"{report.summary.waste_percentage}%",
    )

    summary_table.add_row(
        "Projected Savings",
        f"${report.summary.projected_savings_usd}",
    )

    console.print(summary_table)

    # -----------------------------------------
    # Render Findings
    # -----------------------------------------

    if not report.findings:

        console.print(
            "\n[bold green]No findings detected.[/bold green]"
        )

        raise typer.Exit()

    findings_table = Table(
        title="Findings"
    )

    findings_table.add_column(
        "Severity",
        style="bold",
    )

    findings_table.add_column(
        "Category",
    )

    findings_table.add_column(
        "Title",
    )

    findings_table.add_column(
        "Token Impact",
        justify="right",
    )

    findings_table.add_column(
        "Recommendation",
    )

    for finding in report.findings:

        severity_color = {
            Severity.CRITICAL: "red",
            Severity.WARNING: "yellow",
            Severity.INFO: "blue",
        }.get(
            finding.severity,
            "white",
        )

        findings_table.add_row(
            f"[{severity_color}]"
            f"{finding.severity.value.upper()}"
            f"[/{severity_color}]",
            finding.category.value,
            finding.title,
            str(finding.token_impact or 0),
            finding.recommendation or "-",
        )

    console.print()
    console.print(findings_table)
    console.print()


if __name__ == "__main__":

    app()