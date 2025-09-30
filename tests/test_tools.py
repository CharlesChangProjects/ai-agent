import unittest
from unittest.mock import patch
from packages.tools.web_search import WebSearchTool
from packages.tools.base import ToolInput

class TestWebSearchTool(unittest.TestCase):
    @patch('requests.get')
    def test_search_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "organic_results": [{"title": "Test", "link": "#", "snippet": "..."}]
        }
        tool = WebSearchTool(api_key="test")
        result = tool.run(ToolInput(input="测试"))
        self.assertIn("Test", result)