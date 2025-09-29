import requests
from .base import BaseTool, ToolInput

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "使用Google搜索获取最新信息"

    def execute(self, input: ToolInput) -> str:
        params = {
            "q": input.input,
            "api_key": "YOUR_API_KEY",
            "num": 3
        }
        response = requests.get("https://serpapi.com/search", params=params)
        return str(response.json()["organic_results"][:3])