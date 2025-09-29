from langchain.chains import HyDEChain
from langchain.retrievers import BaseRetriever
from typing import List

from langchain_core.documents import Document


class HydeRetriever(BaseRetriever):
    def __init__(self, vectorstore, llm):
        self.vectorstore = vectorstore
        self.hyde_chain = HyDEChain.from_llm(llm)

    def get_relevant_documents(self, query: str) -> List[Document]:
        """HyDE增强检索"""
        hyde_doc = self.hyde_chain.run(query)
        return self.vectorstore.similarity_search(hyde_doc, k=5)