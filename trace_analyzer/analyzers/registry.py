from trace_analyzer.analyzers.redundancy import (
    RedundancyAnalyzer,
)
from trace_analyzer.analyzers.token_efficiency import (
    TokenEfficiencyAnalyzer,
)

ALL_ANALYZERS = [
    RedundancyAnalyzer(),
    TokenEfficiencyAnalyzer(),
]