from abc import ABC, abstractmethod
from typing import Dict, Any

from langchain.schema import Document


class BaseMemory(ABC):
    @abstractmethod
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        pass

    @abstractmethod
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        pass


class VectorMemory(BaseMemory):
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.buffer = []

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        """保存交互记录到向量库"""
        text = f"Input: {inputs}\nOutput: {outputs}"
        self.buffer.append(Document(page_content=text))
        if len(self.buffer) > 10:  # 批量插入
            self.vectorstore.add_documents(self.buffer)
            self.buffer = []

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """检索相关记忆"""
        query = inputs.get("input", "")
        docs = self.vectorstore.similarity_search(query, k=3)
        return {"history": [doc.page_content for doc in docs]}