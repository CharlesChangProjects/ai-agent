from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional

class ToolInput(BaseModel):
    input: str
    session_id: Optional[str] = None

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """工具的唯一标识符"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """工具的详细描述"""
        pass

    @abstractmethod
    def is_suitable(self, query: str) -> bool:
        """判断是否适合处理当前查询"""
        pass

    @abstractmethod
    def run(self, input: ToolInput) -> str:
        """执行工具的核心逻辑"""
        pass

    def to_langchain_tool(self) -> dict:
        """转换为LangChain兼容格式"""
        return {
            "name": self.name,
            "func": lambda x: self.run(ToolInput(input=x)),
            "description": self.description
        }