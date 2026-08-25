from abc import ABC, abstractmethod
from typing import Any


class InvestigationTool(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, **kwargs: Any) -> dict[str, Any]:
        pass