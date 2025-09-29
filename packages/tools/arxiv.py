import arxiv
from packages.tools.base import BaseTool


class ArxivSearchTool(BaseTool):
    name = "arxiv_search"
    description = "搜索arXiv学术论文"

    def is_suitable(self, query: str) -> bool:
        return any(keyword in query.lower() for keyword in ["论文", "研究", "arxiv"])

    def run(self, query: str) -> str:
        search = arxiv.Search(
            query=query,
            max_results=3,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = []
        for result in search.results():
            results.append(
                f"标题: {result.title}\n"
                f"作者: {', '.join(a.name for a in result.authors)}\n"
                f"摘要: {result.summary[:200]}..."
            )
        return "\n\n".join(results)