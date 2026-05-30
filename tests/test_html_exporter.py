from pathlib import Path

from trace_analyzer.report.html_exporter import (
    HTMLReportExporter,
)
from trace_analyzer.report.generator import (
    ReportGenerator,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
)


def test_html_report_created():

    trace = NormalizedTrace(
        trace_id="test-trace",
    )

    report = ReportGenerator().generate(
        trace=trace,
        findings=[],
    )

    output_file = Path(
        "test_report.html"
    )

    exporter = HTMLReportExporter()

    exporter.export(
        report,
        str(output_file),
    )

    assert output_file.exists()

    output_file.unlink()