import hashlib
import os
from ai.utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def get_file_md5_hex(filepath: str): # 获取文件的md5的十六进制字符型串
    if not os.path.exists(filepath):
        logger.error(f"Agent:[md5计算]文件{filepath}不存在")
        return None
    if not os.path.isfile(filepath):
        logger.error(f"Agent:[md5计算]路径{filepath}不是文件")
        return None

    md5_obj = hashlib.md5()

    chunk_size = 4096   # 4KB分片，避免文件太大爆内存
    try:
        with open(filepath, 'rb') as f:  # 二进制读取
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"Agent:[md5计算]文件{filepath}计算失败，错误信息：{str(e)}")
        return None

def listdir_with_allowed_type(path: str, allowed_types: tuple[str]): # 返回文件内的文件列表（允许的文件后缀）
    files = []

    if not os.path.isdir(path):
        logger.error(f"Agent:[获取文件列表]路径{path}不是文件夹")
        return []

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))

    return tuple(files)

def pdf_loader(filepath: str, password: str = None) -> list[Document]:
    return PyPDFLoader(filepath, password).load()

def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding="utf-8").load()