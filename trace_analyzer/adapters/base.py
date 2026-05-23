from abc import ABC, abstractmethod
from typing import Any

from trace_analyzer.schema.trace import NormalizedTrace


class TraceAdapter(ABC):
    """
    Base interface for all trace adapters.

    Every adapter converts framework-specific
    traces into the unified NormalizedTrace format.
    """

    @abstractmethod
    def can_handle(self, raw_trace: Any) -> bool:
        """
        Determine whether this adapter
        can parse the provided trace.
        """
        pass

    @abstractmethod
    def parse(self, raw_trace: Any) -> NormalizedTrace:
        """
        Convert raw trace into NormalizedTrace.
        """
        pass