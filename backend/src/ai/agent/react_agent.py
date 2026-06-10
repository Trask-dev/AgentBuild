from ai.agent.tools import agent_tools
from ai.agent.tools.middleware import monitor_tool, log_before_model
from ai.model.factory import chat_model
from langchain.agents import create_agent

# 工具名称到函数的映射表
TOOL_REGISTRY = {
    "get_current_time": agent_tools.get_current_time,
    "calculator": agent_tools.calculator,
    "web_search": agent_tools.web_search,
    "get_weather": agent_tools.get_weather,
}


def resolve_tools(tool_names: list, kb_id: int = None) -> list:
    """将工具名称列表转换为实际的工具函数"""
    resolved = []

    # 解析用户选择的工具
    for name in (tool_names or []):
        if name in TOOL_REGISTRY:
            resolved.append(TOOL_REGISTRY[name])

    # 条件性添加 RAG 工具
    if kb_id is not None:
        resolved.append(agent_tools.get_rag_tool(kb_id))

    return resolved

class ReactAgent:
    def __init__(self, model_name, tools, kb_id, system_prompt, api_key, base_url):
        # 解析工具名称为实际函数
        all_tools = resolve_tools(tools, kb_id)

        self.agent = create_agent(
            model=chat_model(model_name, api_key, base_url),
            system_prompt=system_prompt,
            tools=all_tools,
            middleware=[monitor_tool, log_before_model],
        )

    def execute_stream(self, query: str, history_messages: list = None):
        messages = history_messages or []
        messages.append({"role": "user", "content": query})
        input_dict = {"messages": messages}

        for chunk in self.agent.stream(input_dict, stream_mode="values", context={"report": False}):
            latest_message = chunk["messages"][-1]
            content = latest_message.content
            if content:
                yield content