from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import openai
import os
from dotenv import load_dotenv
from .models import Base, ChatMessage
from .schemas import MessageCreate, MessageResponse
from typing import List

load_dotenv()

app = FastAPI(title="AI OS Chat API")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库配置
DATABASE_URL = "sqlite+aiosqlite:///./chat.db"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# OpenAI配置
openai.api_key = os.getenv("OPENAI_API_KEY")

# 启动时创建数据库表
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 依赖注入
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/chat/", response_model=MessageResponse)
async def create_chat(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    try:
        # 调用OpenAI API
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message.content}
            ]
        )
        
        ai_response = response.choices[0].message.content

        # 存储用户消息
        user_message = ChatMessage(
            role="user",
            content=message.content
        )
        db.add(user_message)
        
        # 存储AI响应
        ai_message = ChatMessage(
            role="assistant",
            content=ai_response
        )
        db.add(ai_message)
        
        await db.commit()

        return MessageResponse(
            id=ai_message.id,
            content=ai_response,
            role="assistant",
            created_at=ai_message.created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/", response_model=List[MessageResponse])
async def get_chat_history(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(ChatMessage).order_by(ChatMessage.created_at))
        messages = result.scalars().all()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 