from langchain_core.tools import tool
from ai.rag.vector_store import VectorStoreService


def get_rag_tool(kb_id):
    @tool(description="从RAG本地知识库中检索信息", return_direct=True)
    def rag_tool(query: str):
        vector_store = VectorStoreService(kb_id)
        retriever = vector_store.get_retriever()
        docs = retriever.invoke(query)

        print("=" * 50)
        print(f"[RAG检索] 查询关键词: {query}")
        print(f"[RAG检索] 检索到 {len(docs)} 条文档")
        print("=" * 50)

        if not docs:
            print("[RAG检索] 未找到相关内容")
            return "未找到相关知识库内容"

        context = ""
        for i, doc in enumerate(docs, 1):
            content = doc.page_content

            print(f"\n[文档{i}] 内容长度: {len(content)} 字符")
            print(f"[文档{i}] 前200字符: {content[:200]}...")
            print(f"[文档{i}] 元数据: {doc.metadata}")

            context += f"【参考资料{i}】:参考资料:{doc.page_content} | 参考元数据:{doc.metadata}\n"
            print("=" * 50)
        return context

    return rag_tool