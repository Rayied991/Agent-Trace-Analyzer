import json

from trace_analyzer.adapters.json_adapter import JSONTraceAdapter


def test_json_adapter_parses_trace():

    with open(
        "tests/fixtures/sample_trace.json",
        "r",
        encoding="utf-8"
    ) as f:
        raw_trace = json.load(f)

    adapter = JSONTraceAdapter()

    trace = adapter.parse(raw_trace)

    assert trace.trace_id == "trace_001"
    assert trace.agent_name == "weather-agent"
    assert len(trace.steps) == 3
    assert trace.total_tokens == 305