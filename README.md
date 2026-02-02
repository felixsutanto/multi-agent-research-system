---
title: Multi-Agent Research System
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.14.0
app_file: app.py
pinned: false
license: mit
---

# 🔬 Multi-Agent Research System

> An AI-powered multi-agent system where specialized agents collaborate to conduct comprehensive research, synthesize findings, and produce high-quality reports with citations.

## ✨ Features

- **5 Specialized Agents**: Planner, Researcher, Analyst, Synthesizer, Critic
- **Free LLM**: Uses Groq's Llama 3.3 70B (free tier)
- **Web Search**: Tavily API (1000 free searches/month)
- **Quality Control**: Automatic revision loop with RAG Triad evaluation
- **Web Interface**: Easy-to-use Gradio UI

## 🚀 How to Use

1. Enter your research question in the text box
2. Click "🚀 Start Research"
3. Wait 2-3 minutes while agents work together
4. Get a comprehensive report with citations!

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

This Space uses the following free APIs:

| API | Purpose | Get Key |
|-----|---------|---------|
| Groq | LLM (Llama 3.3 70B) | [console.groq.com](https://console.groq.com) |
| Tavily | Web Search | [tavily.com](https://tavily.com) |

Secrets are configured in Space Settings → Repository secrets.

## 📊 Evaluation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Context Relevance | >0.80 | Retrieved docs match query |
| Groundedness | >0.90 | Claims supported by sources |
| Answer Relevance | >0.85 | Answer addresses question |

## 🛠️ Local Development

```bash
# Clone repo
git clone https://github.com/felixsutanto/multi-agent-research-system
cd multi-agent-research-system

# Install dependencies
python -m uv sync

# Add .env with API keys
echo "GROQ_API_KEY=your_key" > .env
echo "TAVILY_API_KEY=your_key" >> .env

# Run Gradio app
python -m uv run python app.py
```

## 📝 License

MIT

---

**GitHub**: [felixsutanto/multi-agent-research-system](https://github.com/felixsutanto/multi-agent-research-system)
