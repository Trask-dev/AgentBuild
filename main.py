from fastapi import FastAPI
from api.session_router import router as session_router
from api.agent_router import router as agent_router
from api.rag_router import router as rag_router
from core.db import engine, Base
from core.config import settings

# 自动创建数据库表（第一次运行自动生成agent.db）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Agent智能体搭建平台")
# 注册路由
app.include_router(agent_router)
app.include_router(rag_router)
app.include_router(session_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)