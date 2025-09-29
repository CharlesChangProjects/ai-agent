from abc import ABC, abstractmethod
from pydantic import BaseModel

class ToolInput(BaseModel):
    input: str

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, input: ToolInput) -> str:
        pass