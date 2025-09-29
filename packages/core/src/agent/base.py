from typing import Dict, Any, List
from langchain.agents import AgentExecutor, Tool
from langchain_core.language_models import BaseLanguageModel

class AIAgent(AgentExecutor):
    def __init__(
        self,
        llm: BaseLanguageModel,
        tools: List[Tool],
        memory: 'BaseMemory',
        agent_type: str = "openai-tools"
    ):
        self.llm = llm
        self.tools = tools
        self.memory = memory
        self.agent_type = agent_type
        super().__init__(
            tools=tools,
            llm=llm,
            memory=memory,
            agent_type=agent_type
        )

    def add_custom_tool(self, tool: Tool):
        """动态添加工具"""
        self.tools.append(tool)

    def run_pipeline(self, input_text: str) -> Dict[str, Any]:
        """执行完整处理流程"""
        return {
            "input": input_text,
            "output": self.run(input_text),
            "memory": self.memory.load_memory_variables({})
        }