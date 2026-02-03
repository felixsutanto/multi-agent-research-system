<<<<<<< HEAD
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

=======
# Multi-Agent Research System - Frontend

A modern, production-ready Next.js 15 frontend for the Multi-Agent Research System, featuring real-time WebSocket communication, interactive visualizations, and a beautiful user interface.

## 🌟 Features

- **Real-Time Streaming**: Watch AI agents collaborate in real-time via WebSocket
- **Interactive UI**: Beautiful, responsive interface with dark/light mode
- **Agent Timeline**: Live visualization of agent activities and status
- **Streaming Reports**: Progressive report generation with collapsible sections
- **Quality Metrics**: RAG Triad scores, token usage, and cost tracking
- **Preset Templates**: 8 pre-built research query templates
- **Export Capabilities**: Download reports as Markdown
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Backend API running (local or Hugging Face)

### Installation

```bash
# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL

# Run development server
npm run dev

# Open http://localhost:3000
```

### Build for Production

```bash
# Create optimized production build
npm run build

# Start production server
npm start
```

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Landing page
│   └── research/          # Research interface
├── components/
│   ├── ui/                # shadcn/ui components
│   ├── layout/            # Navbar, ThemeToggle
│   ├── research/          # Research-specific components
│   └── shared/            # Shared providers
├── hooks/                 # Custom React hooks
│   └── useResearch.ts    # Main research hook
├── lib/                   # Utilities and configuration
│   ├── types.ts          # TypeScript definitions
│   ├── api.ts            # API client
│   ├── websocket.ts      # WebSocket client
│   └── utils.ts          # Helper functions
└── data/                  # Static data
    └── presets.ts        # Research templates
```

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the root directory:

```bash
# Backend API URL (local development)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Or use your Hugging Face deployment
# NEXT_PUBLIC_API_URL=https://your-space.hf.space
```

### Customization

- **Theme Colors**: Edit `src/app/globals.css`
- **Presets**: Add templates in `src/data/presets.ts`
- **API Endpoints**: Modify `src/lib/api.ts`

## 🎨 Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Animations**: Framer Motion
- **Data Fetching**: TanStack Query (React Query)
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts
- **Icons**: Lucide React
- **Notifications**: Sonner

## 📱 Components

### ResearchForm
Interactive form with validation, preset templates, and keyboard shortcuts.

### AgentTimeline
Real-time visualization of agent activities with smooth animations.

### StreamingReport
Progressive report display with collapsible sections and citations.

### MetricsDashboard
Analytics dashboard showing quality scores, token usage, and costs.

## 🔌 API Integration

The frontend connects to the backend via:

- **REST API**: For starting research sessions
- **WebSocket**: For real-time updates and streaming

### Expected Backend Endpoints

```
POST   /api/research         # Start research
GET    /api/research/:id     # Get session details
GET    /api/research         # List all sessions
DELETE /api/research/:id     # Delete session
WS     /ws/research/:id      # WebSocket connection
```

## 🌐 Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variable: `NEXT_PUBLIC_API_URL`
4. Deploy automatically

### Other Platforms

The app can be deployed to any platform supporting Next.js:
- Netlify
- AWS Amplify
- Google Cloud Run
- Docker

## 🧪 Development

```bash
# Run development server with Turbopack
npm run dev

# Type check
npm run type-check

# Lint
npm run lint

# Format code
npm run format
```

## 📊 Performance

- **Lighthouse Score**: 90+ across all categories
- **Bundle Size**: ~400KB (gzipped)
- **First Load**: <2s on 3G
- **Interactive**: <1s

## 🐛 Troubleshooting

### WebSocket Connection Failed
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings on backend
- Ensure backend WebSocket endpoint is accessible

### Build Errors
- Clear `.next` folder: `rm -rf .next`
- Reinstall dependencies: `npm clean-install`
- Check Node.js version: `node --version` (should be 18+)

### Styles Not Loading
- Restart dev server
- Clear browser cache
- Check Tailwind CSS configuration

>>>>>>> 611a0f83dd86605ce45dad5783be3407e1a524a5
## 📝 License

MIT

<<<<<<< HEAD
---

**GitHub**: [felixsutanto/multi-agent-research-system](https://github.com/felixsutanto/multi-agent-research-system)
=======
## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- GitHub Issues
- Documentation: `/docs`

---

**Built with ❤️ using Next.js 15 and TypeScript**
>>>>>>> 611a0f83dd86605ce45dad5783be3407e1a524a5
