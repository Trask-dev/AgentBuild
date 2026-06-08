from langchain.agents import create_agent
from ai.model.factory import chat_model
from ai.agent.tools.agent_tools import get_rag_tool
from ai.agent.tools.middleware import monitor_tool, log_before_model

class ReactAgent:
    def __init__(self, model_name, tools, kb_id, system_prompt, api_key, base_url):
        # 只在有 kb_id 时添加 RAG 工具
        all_tools = [get_rag_tool(kb_id)] if kb_id is not None else []
        all_tools += (tools or [])

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
            yield latest_message.content.strip() + "\n"
