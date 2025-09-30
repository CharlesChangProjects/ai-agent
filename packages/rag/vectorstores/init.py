from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os

def init_vectorstore(db_path: str = "./data/vectorstore"):
    """初始化并返回向量数据库实例"""
    embedding = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={'device': 'cpu'}
    )
    return Chroma(
        persist_directory=db_path,
        embedding_function=embedding
    )