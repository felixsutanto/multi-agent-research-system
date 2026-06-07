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

An AI-powered multi-agent research system designed to conduct comprehensive, high-quality, autonomous research. The system features a robust **Python (FastAPI) Backend** orchestrating multiple specialized agents and a modern, responsive **Next.js 15 Frontend** with real-time WebSocket streaming, interactive timelines, and detailed quality dashboards.

> [!NOTE]
> This project is designed as a production-grade demonstration for the AI Engineering track, showcasing multi-agent collaboration, WebSocket streaming, RAG evaluation, Docker containerization, CI/CD, and serverless hosting.

---

## 🌟 Key Features

### 🧠 Python Backend (Multi-Agent Orchestration)
- **5 Specialized Collaborative Agents**: Planner, Researcher, Analyst, Synthesizer, and Critic.
- **Agentic RAG & Web Search**: Real-time information retrieval using Tavily API and content scraping.
- **Secure Sandbox Execution**: Python REPL tool allowing agents to run calculations and analysis dynamically.
- **RAG Triad Quality Control**: Multi-dimensional evaluation loop scoring Context Relevance, Groundedness, and Answer Relevance.
- **Free-Tier Optimization**: Powered by Groq's Llama 3.3 70B and free API resources.

### 🎨 Next.js Frontend (Interactive UI)
- **Real-Time Streaming**: Live WebSocket-driven updates displaying the active agent and research progress.
- **Interactive Visualizations**: Beautiful timeline tracking agent activities, metrics, and token costs.
- **Premium Aesthetics**: Fully responsive layout featuring sleek dark/light modes, glassmorphism, and smooth animations.
- **Interactive Templates**: Pre-built presets for common research topics.
- **Export Formats**: One-click download of generated research reports as formatted Markdown files.

---

## 🏗️ System Architecture & Workflow

The system uses a state graph to manage agent transitions. The workflow is iterative: if the **Critic** flags issues in the draft report, it is sent back to the **Researcher** or **Analyst** for refinement.

```
User Query ──> [Planner] ──> [Researcher] ──> [Analyst] ──> [Synthesizer] ──> [Critic] ──> Report Approved?
                                  ^              |              |              |
                                  |              v              |              ├──> Yes ──> Final Report
                                  └──────────────┴──────────────┴──────────────┘ No (Revise)
```

| Agent | Core Responsibility | Key Tools Used |
| :--- | :--- | :--- |
| **Planner** | Decomposes the query into a multi-step research plan. | LLM Reasoner |
| **Researcher** | Performs search queries, scrapes web pages, and gathers context. | Tavily Search, Web Scraper |
| **Analyst** | Performs data analysis, parses numerical data, and solves math equations. | Python REPL Sandbox |
| **Synthesizer** | Merges agent outputs, resolves contradictions, and drafts the report. | Markdown Synthesizer |
| **Critic** | Evaluates the report using the RAG Triad, proposing revisions if needed. | TruLens-based Evaluator |

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Core** | FastAPI & Python 3.11 | High-performance API hosting REST and WebSocket endpoints. |
| **Agent Framework** | LangGraph & Custom State Graph | Manages execution order, memory, and routing. |
| **LLM Provider** | Groq (Llama 3.3 70B) | High-speed, free-tier LLM API. |
| **Frontend Core** | Next.js 15 & React 19 | Production-ready framework using App Router. |
| **Styling** | Tailwind CSS & shadcn/ui | Beautiful, responsive, themeable design system. |
| **Animations** | Framer Motion | Smooth state transitions and micro-animations. |
| **State & Fetching**| TanStack Query & WebSockets | Manage server-side caching and real-time streams. |

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended Python package manager)
- API Keys:
  - **Groq API Key**: Get one at [console.groq.com](https://console.groq.com)
  - **Tavily API Key**: Get one at [tavily.com](https://tavily.com)

### 1. Clone & Environment Configuration

Clone the repository:
```bash
git clone https://github.com/felixsutanto/multi-agent-research-system.git
cd multi-agent-research-system
```

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Create a `.env.local` file in the root directory (for Next.js frontend):
```env
NEXT_PUBLIC_API_URL=http://localhost:7860
```

### 2. Run the Backend API

Using `uv`:
```bash
# Sync dependencies
python -m uv sync

# Start FastAPI server
python -m uv run python app.py
```
The API server will run at `http://localhost:7860`.

### 3. Run the Frontend App

```bash
# Install dependencies
npm install

# Start Next.js development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📊 Evaluation & Quality Metrics

To ensure the output is high-quality and free of hallucination, the system evaluates drafts against the **RAG Triad** before final approval:

| Metric | Target | Focus Area |
| :--- | :--- | :--- |
| **Context Relevance** | `> 0.80` | Ensures research documents retrieved by the Researcher match the original query. |
| **Groundedness** | `> 0.90` | Verifies that all claims made in the report are backed by web sources (no hallucinations). |
| **Answer Relevance** | `> 0.85` | Ensures the final synthesized report directly and fully answers the user query. |

If any score falls below the threshold, the **Critic** instructs the agents to revise, with a maximum of `5` iterations to avoid infinite loops.

---

## 📦 Deployment

This project is configured for cloud deployment:
- **Backend**: Deployed to Hugging Face Spaces (or any Docker-supported container platform).
- **Frontend**: Deployed to Vercel.

For step-by-step instructions on deploying the application to Vercel, Docker, AWS, or Netlify, please refer to the [Deployment Guide](./DEPLOYMENT.md).

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
