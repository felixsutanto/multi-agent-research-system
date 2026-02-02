# Multi-Agent Research System

> An AI-powered multi-agent system where specialized agents collaborate to conduct comprehensive research, synthesize findings, and produce high-quality reports with citations.

## ✨ Features

- **5 Specialized Agents**: Planner, Researcher, Analyst, Synthesizer, Critic
- **Free LLM**: Uses Groq's Llama 3.3 70B (free tier)
- **Web Search**: Tavily API (1000 free searches/month)
- **Quality Control**: Automatic revision loop with RAG Triad evaluation
- **API Ready**: FastAPI with REST and WebSocket endpoints

## 🚀 Quick Start

### 1. Get Free API Keys

| Service | Free Tier | Sign Up |
|---------|-----------|---------|
| **Groq** | Llama 3.3 70B (unlimited*) | [console.groq.com](https://console.groq.com) |
| **Tavily** | 1000 searches/month | [tavily.com](https://tavily.com) |

### 2. Setup

```bash
# Clone and enter directory
cd "Multi-Agent Research System"

# Create .env file with your API keys
echo "GROQ_API_KEY=your_groq_key" > .env
echo "TAVILY_API_KEY=your_tavily_key" >> .env

# Install dependencies
python -m uv sync
```

### 3. Run

```bash
python -m uv run uvicorn src.api.main:app --reload
```

### 4. Test

```powershell
# PowerShell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/research" `
  -Method POST -ContentType "application/json" `
  -Body '{"query": "What are the benefits of renewable energy?"}'
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

## 📁 Project Structure

```
src/
├── agents/          # 5 AI agents
├── tools/           # Web search, vector DB, Python REPL
├── graph/           # LangGraph workflow
├── evaluation/      # RAG Triad metrics
├── api/             # FastAPI endpoints
└── utils/           # Config, logging, LLM provider
```

## 🔧 Configuration

Edit `config/config.yaml`:

```yaml
llm:
  model: "llama-3.3-70b-versatile"  # Groq model
  temperature: 0.0

agents:
  max_iterations: 3  # Max revision loops
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/research` | POST | Conduct research |
| `/ws/research` | WebSocket | Streaming updates |

## 🚢 Deploy (Free)

### Render.com

1. Push to GitHub
2. Create Web Service at [render.com](https://render.com)
3. Add environment variables
4. Deploy!

### Docker

```bash
docker-compose up --build
```

## 📊 Evaluation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Context Relevance | >0.80 | Retrieved docs match query |
| Groundedness | >0.90 | Claims supported by sources |
| Answer Relevance | >0.85 | Answer addresses question |

## 📝 License

MIT
