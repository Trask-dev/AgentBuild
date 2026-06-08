"""
总结服务类：用户提问，搜索参考资料，将提问和参考资料提交给模型，让模型总结回复
"""
from ai.model.factory import chat_model
from ai.rag.vector_store import VectorStoreService
from ai.utils.prompt_loader import load_rag_prompt
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt

class RagSummarizeService(object):
    def __init__(self, kb_id, model_name, api_key, base_url):
        self.vector_store = VectorStoreService(kb_id)
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model(model_name, api_key, base_url)
        self.chain = self._init_chain()

    def _init_chain(self):
        chain = (
                self.prompt_template
                | print_prompt
                | self.model
                | StrOutputParser()
        )
        return chain

    def retriever_docs(self, query: str) -> list[Document]: #检索文档
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        context_docs = self.retriever_docs(query)
        context = ""
        counter = 0
        for doc in context_docs:
            counter += 1
            context += f"【参考资料{counter}】:参考资料:{doc.page_content} | 参考元数据:{doc.metadata}\n"
        return self.chain.invoke(
            {
                "input": query,
                "context": context,
            }
        )
