# AI OS 智能操作系统

一个基于人工智能的智能操作系统，集成语音交互、自然语言处理和多种智能服务。

## 系统概述

本系统是一个智能化操作系统，通过语音交互和图形界面为用户提供智能化的日常任务处理。系统集成了语音识别、自然语言理解、对话管理等多个人工智能模块，并提供邮件处理、新闻聚合、日程管理等实用功能。

## 核心功能

- 语音交互：支持语音输入和语音反馈
- 智能对话：基于GPT-4的自然语言理解和生成
- 邮件管理：智能邮件处理和管理
- 新闻聚合：自动新闻抓取和摘要
- 日程管理：智能日程规划和提醒
- 多设备支持：支持手机、电脑、智能音箱等设备

## 技术架构

### 前端技术
- React Native（移动端和Web端）
- Expo
- WebSocket（实时数据推送）

### 后端技术
- Python FastAPI
- SQLite + SQLAlchemy
- JWT 认证
- OAuth 认证

### AI 模块
- Whisper（语音识别）
- GPT-4（自然语言处理）
- Edge TTS/Microsoft TTS（语音合成）
- Rasa/LangChain（对话管理）

## 系统要求

- Python 3.8+
- Node.js 14+
- SQLite 3
- 麦克风和扬声器设备

## 快速开始
python -m venv .venv
source .venv/bin/activate  # Windows 用 `.venv\Scripts\activate`
pip install -r requirements.txt
uvicorn app.main:app --reload