from ai.utils.config_handler import prompts_conf
from ai.utils.logger_handler import logger
from ai.utils.path_tool import get_abs_path

def load_rag_prompt():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_prompt_path"])
    except KeyError as e:
        logger.error(f"agent:[load_rag_prompt]在yaml配置项中没有rag_summarize_prompt_path配置项")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"agent:[load_rag_prompt]解析RAG总结提示词出错：{str(e)}")
        raise e
