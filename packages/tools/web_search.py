from .base import BaseTool, ToolInput
import requests
import json

class WebSearchTool(BaseTool):
    name = "web_search"
    description = "使用SerpAPI进行实时网络搜索"

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPAPI_KEY")

    def is_suitable(self, query: str) -> bool:
        return any(kw in query.lower() for kw in ["最新", "新闻", "搜索"])

    def run(self, input: ToolInput) -> str:
        params = {
            "q": input.input,
            "api_key": self.api_key,
            "num": 3,
            "hl": "zh"
        }
        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json().get("organic_results", [])
        return json.dumps([{
            "title": r.get("title"),
            "link": r.get("link"),
            "snippet": r.get("snippet")
        } for r in results], ensure_ascii=False)