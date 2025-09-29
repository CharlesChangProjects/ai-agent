from typing import Any, List
from langchain_core.documents import Document

class VectorMemory:
    def __init__(self, vectorstore):
        self.store = vectorstore

    def retrieve(self, query: str) -> List[Document]:
        """基于向量检索的记忆召回"""
        return self.store.similarity_search(query)