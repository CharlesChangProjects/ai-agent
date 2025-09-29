from langchain.chains import HyDEChain


class RAGGenerator:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.hyde_chain = HyDEChain.from_llm(llm)

    def generate(self, query: str) -> str:
        # 1. 生成假设文档
        hyde_doc = self.hyde_chain.run(query)
        # 2. 检索相关文档
        docs = self.retriever.retrieve(hyde_doc)
        # 3. 生成最终答案
        return self._format_output(docs)
