# 工具基类 (tools/base.py)
from langchain.tools import BaseTool


class WebSearchTool(BaseTool):
    name = "web_search"
    description = "Search the web for current information"

    def _run(self, query: str) -> str:
        from serpapi import GoogleSearch
        # 实现搜索逻辑...