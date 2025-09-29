from typing import List

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document

RAG_PROMPT = """
基于以下上下文回答问题：
{context}

问题：{question}
请提供详细且准确的回答："""

class RAGGenerator:
    def __init__(self, llm):
        self.prompt = PromptTemplate(
            template=RAG_PROMPT,
            input_variables=["context", "question"]
        )
        self.chain = LLMChain(llm=llm, prompt=self.prompt)

    def generate(self, question: str, context: List[Document]) -> str:
        context_str = "\n---\n".join([doc.page_content for doc in context])
        return self.chain.run(question=question, context=context_str)