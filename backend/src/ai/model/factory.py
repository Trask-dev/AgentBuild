from ai.utils.config_handler import rag_conf
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


class ChatModelFactory():
    def generator(self, model_name, api_key, base_url) -> BaseChatModel:
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            streaming=True
        )

class EmbeddingFactory():
    def generator(self) -> Embeddings:
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
        )

def chat_model(model_name, api_key, base_url):
    return ChatModelFactory().generator(model_name, api_key, base_url)
embed_model = EmbeddingFactory().generator()