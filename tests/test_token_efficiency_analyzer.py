from trace_analyzer.analyzers.token_efficiency import (
    TokenEfficiencyAnalyzer,
)
from trace_analyzer.schema.trace import (
    NormalizedTrace,
    StepType,
    TraceStep,
)


def test_large_input_detection():

    trace = NormalizedTrace(
        trace_id="trace-large-input",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.LLM_CALL,
            content="Large prompt",
            input_tokens=5000,
            output_tokens=100,
        )
    )

    analyzer = TokenEfficiencyAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 1

    assert findings[0].title == (
        "Large prompt detected"
    )


def test_large_output_detection():

    trace = NormalizedTrace(
        trace_id="trace-large-output",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.LLM_CALL,
            content="Large output",
            input_tokens=100,
            output_tokens=3000,
        )
    )

    analyzer = TokenEfficiencyAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 1

    assert findings[0].title == (
        "Large output detected"
    )


def test_normal_token_usage():

    trace = NormalizedTrace(
        trace_id="trace-normal",
    )

    trace.add_step(
        TraceStep(
            step_id="1",
            step_type=StepType.LLM_CALL,
            content="Normal step",
            input_tokens=500,
            output_tokens=200,
        )
    )

    analyzer = TokenEfficiencyAnalyzer()

    findings = analyzer.analyze(trace)

    assert len(findings) == 0