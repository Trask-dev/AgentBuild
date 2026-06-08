# 智能体搭建平台

AI 智能体搭建与对话平台，支持自定义智能体、RAG 知识库、流式对话。

## 技术栈

- **后端**: FastAPI + SQLAlchemy + LangChain + ChromaDB
- **LLM**: 通义千问 (DashScope) / OpenAI 兼容接口
- **数据库**: MySQL + ChromaDB (向量库)

## 项目结构

```
├── backend/          # 后端 API 服务
│   ├── ai/           # AI 核心层 (Agent, RAG, 模型工厂)
│   ├── api/          # FastAPI 路由层
│   ├── core/         # 基础设施 (配置, 数据库)
│   ├── models/       # SQLAlchemy 数据模型
│   ├── schemas/      # Pydantic 请求/响应模型
│   ├── services/     # 业务逻辑层
│   ├── utils/        # 工具函数
│   ├── main.py       # 应用入口
│   └── requirements.txt
└── frontend/         # 前端 (待开发)
```

## 快速开始

```bash
cd backend
pip install -r requirements.txt
python main.py
```
