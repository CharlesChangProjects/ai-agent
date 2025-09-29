from typing import Any, List

from langchain.agents import AgentExecutor



class AIAgent(AgentExecutor):
    def __init__(self, tools, llm, memory, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.memory = memory  # 记忆系统
        self.llm = llm  # 语言模型
        self.tools = tools  # 工具集

    def add_memory(self, key: str, value: Any):
        """自定义记忆管理"""
        self.memory.save_context({key: value})



