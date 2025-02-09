# 人工智能 OS 系统架构（技术栈）


1. 用户语音输入 → Whisper（ASR）
2. Whisper 输出文本 → GPT-4o 解析意图（JSON 结构）
3. GPT 解析结果 → NLU (Rasa/spaCy) 校验
4. 若意图确定：
   - 触发相应的 API（邮件、日程、新闻）
   - 返回结果（语音 + 可视化界面）
5. 若意图不确定：
   - 进行确认（语音 or 文字）
   - 允许用户纠正



## 用户层
- **设备**：手机、电脑、智能音箱
- **图形界面**（可选）
  - **APP 开发**：React Native
  - **Web 界面**：React Native

## 前端交互层
- **语音采集**：麦克风（硬件）  
  - **调用方式**：Python + `pyaudio` / `speech_recognition`
- **语音播放**：扬声器（硬件）
  - **调用方式**：Python + `pyttsx3` / `gTTS`

## 语音处理层
- **ASR（语音识别）**：
  - **Whisper（OpenAI）
  - Python + `whisper`
- **NLU（自然语言理解）**：
  - **GPT-4o API**
  - Python + `spacy` / `nltk` / `openai`
- **DM（对话管理）**：
  - Python + `Rasa` 或自定义逻辑（`Langchain` + `LlamaIndex`）
- **NLG（自然语言生成）**：
  - Python + `transformers` / `openai`
- **TTS（文本转语音）**：
  - **Edge TTS（本地）** / **microsoft TTS** / **OpenAI TTS**
  - Python + `edge-tts` / `pyttsx3` / `gTTS`

## 业务服务层
- **邮件**：邮件处理模块
  - Python + `imaplib` / `smtplib`
- **新闻**：新闻抓取与摘要模块
  - Python + chatpgt 联网搜索进行摘要（GPT-4o）
- **日程**：日程/任务管理模块
  - Python + `sqlite3` 存储临时任务
  - 可对接 Google Calendar API
- **其他智能服务**：
  - Python + FastAPI / Flask 作为后端 API

## 后端支撑层
- **数据库**：数据存储与管理
  - SQLite（轻量级存储）+ SQLAlchemy（ORM）
- **安全**：数据安全与隐私保护
  - **JWT 认证**（Python `pyjwt`）
  - **OAuth 认证**（Python `authlib`）
- **API**：第三方 API 接口
  - 邮件服务：IMAP / SMTP
  - 新闻抓取：X API / google news API
  - 日程管理：Google Calendar API
  - AI 交互：OpenAI API 

## 数据流（整体技术栈）

### 用户交互
1. **Node.js + React Native**（APP 端） → **Python FastAPI**（后端）
2. **麦克风录音**（Python `pyaudio`） → **Whisper/Vosk 语音识别**
3. **文本分析（NLU）**（Python `spaCy` / `nltk` / GPT-4o）
4. **任务管理（DM）**（Python `Langchain` / `Rasa`）
5. **TTS 语音合成**（Python `edge-tts` / `pyttsx3`）

### 对话管理调用业务服务
1. **邮件服务**（Python `imaplib` / `smtplib`）
2. **新闻抓取**（Python `newspaper3k` / `BeautifulSoup`）
3. **日程管理**（Python `sqlite3` + Google Calendar API）
4. **其他智能任务**（Python `FastAPI` + `LlamaIndex`）

### 业务服务与后端交互
1. SQLite + SQLAlchemy（数据存储）
2. JWT 认证（Python `pyjwt`）
3. OpenAI API（GPT-4o）
4. OAuth 认证（Google API）

### APP（React Native）数据交互
1. React Native + Expo（前端 UI）
2. REST API（Python FastAPI 提供后端接口）
3. WebSocket（用于实时推送 AI 交互数据）
