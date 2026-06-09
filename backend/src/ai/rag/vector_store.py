import os

from ai.model.factory import embed_model
from ai.utils.config_handler import chroma_conf
from ai.utils.file_handler import txt_loader, pdf_loader, listdir_with_allowed_type, get_file_md5_hex
from ai.utils.logger_handler import logger
from ai.utils.path_tool import get_abs_path
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStoreService:
    def __init__(self, kb_id):
        self.kb_id = kb_id
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=get_abs_path(f"{chroma_conf['persist_directory']}/kb_{self.kb_id}"),
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

    def get_retriever(self):  # 获取向量检索器
        return self.vector_store.as_retriever(
            search_kwargs={"k": chroma_conf["k"]},
        )

    def load_documents(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的 md5 做去重
        :param self:
        :return:
        """

        def check_md5_hex(md5_for_check: str):
            md5_file_path = os.path.join(get_abs_path(chroma_conf['md5_hex_store']), f"kb_{self.kb_id}")
            md5_dir = os.path.dirname(md5_file_path)

            if not os.path.exists(md5_dir):
                os.makedirs(md5_dir, exist_ok=True)

            if not os.path.exists(md5_file_path):
                open(md5_file_path, "w", encoding="utf-8").close()
                return False

            with open(md5_file_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True

                return False

        def save_md5_hex(md5_for_check: str):
            md5_file_path = os.path.join(get_abs_path(chroma_conf['md5_hex_store']), f"kb_{self.kb_id}")
            md5_dir = os.path.dirname(md5_file_path)

            if not os.path.exists(md5_dir):
                os.makedirs(md5_dir, exist_ok=True)

            with open(md5_file_path, "a", encoding="utf-8") as f:
                f.write(md5_for_check + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)

            return []

        allowed_file_path: list[str] = listdir_with_allowed_type(
            os.path.join(get_abs_path(chroma_conf['data_path']), f"kb_{self.kb_id}"),
            tuple(chroma_conf["allow_knowledge_file_type"])
        )

        for path in allowed_file_path:
            # 获取文件的md5
            md5_hex = get_file_md5_hex(path)
            if check_md5_hex(md5_hex):
                logger.info(f"agent:[加载知识库]{path}内容已经存在知识库内，跳过")
                continue
            try:
                doucuments: list[Document] = get_file_documents(path)

                if not doucuments:
                    logger.error(f"agent:[加载知识库]{path}内没有有效内容，跳过")
                    continue

                split_document: list[Document] = self.spliter.split_documents(doucuments)

                if not split_document:
                    logger.error(f"agent:[加载知识库]{path}分片后没有有效内容，跳过")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理好的文件的md5，避免下次重复加载
                save_md5_hex(md5_hex)

                logger.info(f"agent:[加载知识库]{path}内容加载成功")
            except Exception as e:
                # exc_info=True会记录详细的错误堆栈，False仅记录报错信息本身
                logger.error(f"agent:[加载知识库]{path}内容加载失败，错误信息：{str(e)}", exc_info=True)
                continue

if __name__ == '__main__':
    vector_service = VectorStoreService(kb_id = 0)
    vector_service.load_documents()