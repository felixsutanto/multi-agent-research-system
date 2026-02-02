---
title: Multi-Agent Research System
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Multi-Agent Research System

> An AI-powered multi-agent system where specialized agents collaborate to conduct comprehensive research, synthesize findings, and produce high-quality reports with citations.

## ✨ Features

- **5 Specialized Agents**: Planner, Researcher, Analyst, Synthesizer, Critic
- **Free LLM**: Uses Groq's Llama 3.3 70B (free tier)
- **Web Search**: Tavily API (1000 free searches/month)
- **Quality Control**: Automatic revision loop with RAG Triad evaluation
- **API Ready**: FastAPI with REST and WebSocket endpoints

## 🚀 Quick Start

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/research` | POST | Conduct research |
| `/ws/research` | WebSocket | Streaming updates |

### Example Request

```bash
curl -X POST "https://YOUR-SPACE.hf.space/research" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the benefits of renewable energy?"}'
```

## 🏗️ Architecture

```
User Query → Planner → Researcher → Analyst → Synthesizer → Critic → Report
                                                    ↑          ↓
                                                    ←── Revise ←┘
```

| Agent | Role |
|-------|------|
| **Planner** | Decomposes query into research tasks |
| **Researcher** | Executes web searches via Tavily |
| **Analyst** | Performs data analysis with Python |
| **Synthesizer** | Generates report with citations |
| **Critic** | Reviews quality, requests revisions |

## 🔧 Configuration

Set these secrets in your Hugging Face Space settings:

| Secret | Description |
|--------|-------------|
| `GROQ_API_KEY` | Get free at [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | Get free at [tavily.com](https://tavily.com) |

## 📊 Evaluation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Context Relevance | >0.80 | Retrieved docs match query |
| Groundedness | >0.90 | Claims supported by sources |
| Answer Relevance | >0.85 | Answer addresses question |

## 📝 License

MIT
