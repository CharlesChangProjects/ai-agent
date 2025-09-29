from packages.core.src.agent.base import AIAgent
from packages.core.src.memory.manager import VectorMemory
from packages.rag.retrievers.hyde import HydeRetriever
from packages.tools.web_search import WebSearchTool
from langchain.vectorstores import Chroma
from langchain_core.language_models import BaseChatModel
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import requests
import os

# 加载DeepSeek API密钥
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


class DeepSeekLLM(BaseChatModel):
    """DeepSeek API的LangChain兼容封装"""

    def __init__(self, model: str = "deepseek-chat", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature
        self.base_url = "https://api.deepseek.com/v1"
        self.api_key = os.getenv("DEEPSEEK_API_KEY")

    def _generate(self, messages, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            **kwargs
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        return response.json()

    @property
    def _llm_type(self) -> str:
        return "deepseek"


def create_deepseek_retriever(vectorstore, llm):
    """创建基于DeepSeek的HyDE检索器"""

    class DeepSeekHydeChain:
        def __init__(self, llm):
            self.llm = llm

        def run(self, query: str) -> str:
            response = self.llm._generate([{
                "role": "user",
                "content": f"请为以下问题生成假设性文档：\n{query}"
            }])
            return response['choices'][0]['message']['content']

    return HydeRetriever(
        vectorstore=vectorstore,
        llm=DeepSeekHydeChain(llm)
    )


def create_research_agent():
    # 初始化DeepSeek LLM
    llm = DeepSeekLLM(model="deepseek-researcher", temperature=0.5)

    # 配置向量存储
    vectorstore = Chroma(
        persist_directory="./data/vectorstore",
        embedding_function=HuggingFaceEmbeddings()  # 使用开源嵌入模型
    )

    # 构建记忆系统
    memory = VectorMemory(vectorstore)

    # 创建RAG检索器
    retriever = create_deepseek_retriever(vectorstore, llm)

    # 工具集配置
    tools = [
        WebSearchTool().to_langchain_tool(),
        {
            "name": "knowledge_base",
            "func": lambda q: str(retriever.get_relevant_documents(q)),
            "description": "访问本地知识库获取研究资料"
        },
        {
            "name": "arxiv_search",
            "func": lambda q: search_arxiv(q),
            "description": "在arXiv上搜索学术论文"
        }
    ]

    return AIAgent(
        llm=llm,
        tools=tools,
        memory=memory,
        agent_type="structured-chat"  # DeepSeek更适合结构化聊天代理
    )


# arXiv搜索工具函数
def search_arxiv(query: str, max_results: int = 3) -> str:
    import arxiv
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = [f"{r.title}\n{r.summary}" for r in search.results()]
    return "\n\n".join(results)


# 使用示例
if __name__ == "__main__":
    agent = create_research_agent()
    response = agent.run_pipeline(
        "请总结量子计算在密码学中的应用最新进展"
    )
    print("智能体响应：", response["output"])
    print("相关记忆：", response["memory"]["history"])