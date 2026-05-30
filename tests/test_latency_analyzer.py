from trace_analyzer.analyzers.latency import (
    LatencyAnalyzer,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
    StepType,
    TraceStep,
)


def test_slow_step_detected():

    trace = NormalizedTrace(
        trace_id="slow-trace",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.TOOL_CALL,
            content="Search",
            latency_ms=6000,
        )
    )

    analyzer = LatencyAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 1

    assert findings[0].category.value == (
        "latency"
    )


def test_fast_step_not_detected():

    trace = NormalizedTrace(
        trace_id="fast-trace",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.TOOL_CALL,
            content="Search",
            latency_ms=500,
        )
    )

    analyzer = LatencyAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 0