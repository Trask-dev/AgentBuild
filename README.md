# AI Agent 搭建平台

基于 **LangChain ReAct Agent** + **RAG 检索增强生成** 的智能体编排平台。支持用户自定义 Agent 角色、绑定私有知识库、多工具调用、SSE 流式实时对话。

## 功能

- **智能体管理** — 创建/编辑/删除自定义 AI Agent，配置系统提示词、大模型、API Key、工具绑定、知识库
- **流式对话** — SSE 实时打字机效果，支持多轮对话，自动保存历史
- **RAG 知识库** — 上传 TXT/PDF 文档，自动分块→向量化→语义检索，为 Agent 注入领域知识
- **会话管理** — 多会话切换，历史记录查阅，按智能体筛选
- **模型灵活接入** — 支持 OpenAI 兼容 API（通义千问、DeepSeek、GPT 等任意模型）
- **多工具调用** — 内置计算器、网络搜索、天气查询、RAG 知识检索等工具，Agent 可动态选择调用

## 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | Vue 3 · Vite · Element Plus · Pinia · Axios |
| 后端 | FastAPI · SQLAlchemy · Pydantic |
| AI | LangChain · ReAct Agent · ChromaDB |
| 数据库 | MySQL + ChromaDB（向量库） |
| LLM | 通义千问 DashScope（兼容 OpenAI API） |

## 项目结构

```
智能体搭建平台/
├── backend/
│   ├── src/
│   │   ├── ai/
│   │   │   ├── agent/         # ReAct Agent + 工具集
│   │   │   ├── model/         # LLM 模型工厂
│   │   │   ├── rag/           # RAG 检索 + 向量存储
│   │   │   ├── config/        # YAML 配置（Agent、Chroma、RAG、Prompts）
│   │   │   ├── prompts/       # Prompt 模板
│   │   │   └── utils/         # 日志、文件处理、配置加载等工具
│   │   ├── api/           # FastAPI 路由（agent、chat、session、rag、tool）
│   │   ├── core/          # 数据库 & 配置
│   │   ├── models/        # SQLAlchemy ORM（agent、session、chat_history、rag、tool）
│   │   ├── schemas/       # Pydantic 请求/响应
│   │   ├── services/      # 业务逻辑（agent、chat、session、rag、tool）
│   │   └── main.py        # 应用入口
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/    # 通用组件
│   │   ├── views/         # 页面视图
│   │   ├── api/           # 接口封装
│   │   ├── stores/        # Pinia 状态
│   │   └── router/        # 路由配置
│   └── package.json
└── docker-compose.yml
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- MySQL 8.0

### 1. 后端

```bash
cd backend
pip install -r requirements.txt

# 配置 .env
cp .env.example .env
# 编辑 .env 填入数据库连接和端口

python src/main.py
```

### 2. 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## API 概览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/agent` | 创建智能体 |
| GET | `/agent` | 获取所有智能体 |
| GET | `/agent/{id}` | 获取单个智能体 |
| PUT | `/agent/{id}` | 更新智能体 |
| DELETE | `/agent/{id}` | 删除智能体 |
| POST | `/rag` | 创建知识库 |
| GET | `/rag` | 获取所有知识库 |
| POST | `/rag/{id}/upload` | 上传文件到知识库 |
| GET | `/tools` | 获取所有可用工具 |
| POST | `/session` | 创建会话 |
| GET | `/session` | 获取会话列表 |
| POST | `/chat/{id}` | 流式对话（SSE） |
| GET | `/chat/{id}/history` | 获取对话历史 |

## 架构

```
用户 → Vue 3 前端 → Vite Proxy → FastAPI 后端
                                       ├── LangChain ReAct Agent
                                       │     ├── LLM（通义千问）
                                       │     └── Tools（计算器·网络搜索·天气查询·RAG检索）
                                       ├── ChromaDB（向量检索）
                                       └── MySQL（业务数据 + 工具注册表）
```
