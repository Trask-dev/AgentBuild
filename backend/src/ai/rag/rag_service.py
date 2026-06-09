from ai.model.factory import chat_model
from ai.rag.vector_store import VectorStoreService
from ai.utils.config_handler import chroma_conf
from ai.utils.prompt_loader import load_rag_prompt
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


def print_prompt(prompt):
    """调试用：打印 prompt 内容"""
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt


class RagService:
    """
    RAG 服务类
    提供两种模式：
    1. 检索模式（retrieve_and_format）- 供 Agent 工具使用
    2. 总结模式（rag_summarize）- 传统 RAG 流程，备用
    """
    
    def __init__(self, kb_id: int, model_name: str = None, api_key: str = None, base_url: str = None):
        self.kb_id = kb_id
        self.vector_store = VectorStoreService(kb_id)
        self.retriever = self.vector_store.get_retriever()
        self.prompt_template_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_template_text)
        self.score_threshold = chroma_conf.get("score_threshold", 0.0)
        
        # 总结模式需要 LLM（可选）
        if model_name and api_key and base_url:
            self.model = chat_model(model_name, api_key, base_url)
            self.chain = self._init_chain()
        else:
            self.model = None
            self.chain = None
    
    def _init_chain(self):
        """初始化总结链（仅总结模式使用）"""
        chain = (
                self.prompt_template
                | print_prompt
                | self.model
                | StrOutputParser()
        )
        return chain
    
    # ==================== 基础检索方法 ====================
    
    def retriever_docs(self, query: str) -> list[Document]:
        """
        检索文档并过滤低相似度结果
        """
        docs = self.retriever.invoke(query)
        
        # 过滤低相似度结果
        if self.score_threshold > 0:
            filtered_docs = []
            for doc in docs:
                # ChromaDB 返回的 metadata 中包含 'distance' 或 'score'
                distance = doc.metadata.get('distance', 0)
                # distance 越小表示越相似，转换为相似度分数
                score = 1 - distance if distance < 1 else 0
                
                if score >= self.score_threshold:
                    filtered_docs.append(doc)
            
            return filtered_docs
        
        return docs
    
    # ==================== 检索模式（Agent 工具用）====================
    
    def retrieve_and_format(self, query: str) -> str:
        """
        检索知识库并格式化结果
        """
        # 复用 retriever_docs 方法
        docs = self.retriever_docs(query)
        
        if not docs:
            return "未找到相关知识库内容"
        
        # 组装上下文
        context = ""
        for i, doc in enumerate(docs, 1):
            content = doc.page_content
            metadata = doc.metadata
            
            # 提取引用信息
            filename = metadata.get('source', '未知文件')
            chunk_idx = metadata.get('chunk_index', 0) + 1
            
            context += f"【参考资料{i} - 文件:{filename} 片段:{chunk_idx}】:{doc.page_content}\n"
        
        # 使用模板格式化
        formatted_prompt = self.prompt_template.format(
            context=context,
            input=query
        )
        
        return formatted_prompt
    
    # ==================== 总结模式（传统 RAG，备用）====================
    
    def rag_summarize(self, query: str) -> str:
        """
        检索并总结（传统 RAG 模式）
        """
        if not self.chain:
            raise RuntimeError("总结模式未初始化，需要提供 model_name, api_key, base_url")

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

