from typing import List
from langchain.schema import Document
from langchain.retrievers import BM25Retriever

class HybridRetriever:
    def __init__(self, vector_retriever, text_corpus: List[str]):
        self.vector = vector_retriever
        self.bm25 = BM25Retriever.from_texts(text_corpus)

    def retrieve(self, query: str, top_k: int = 5) -> List[Document]:
        # 向量检索
        vector_docs = self.vector.similarity_search(query, k=top_k)
        # 关键词检索
        bm25_docs = self.bm25.get_relevant_documents(query)[:top_k]
        # 去重合并
        all_docs = {doc.page_content: doc for doc in vector_docs + bm25_docs}
        return list(all_docs.values())[:top_k]