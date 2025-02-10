from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import pytest
import os
from dotenv import load_dotenv
from app.main import app, get_db
from app.models import Base

# 测试数据库配置
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 创建测试客户端
client = TestClient(app)

# 测试依赖覆盖
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
async def setup_db():
    # 设置测试数据库
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 清理测试数据库
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

def test_create_chat():
    response = client.post(
        "/chat/",
        json={"content": "你好"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "content" in data
    assert "role" in data
    assert data["role"] == "assistant"

def test_get_chat_history():
    # 先创建一些测试数据
    client.post("/chat/", json={"content": "测试消息1"})
    client.post("/chat/", json={"content": "测试消息2"})
    
    response = client.get("/chat/history/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2 