# Deployment Guide: Multi-Agent Research System

This guide outlines the production deployment process for the Multi-Agent Research System. The architecture separates the application into a **Python (FastAPI) Backend** (optimized for Hugging Face Spaces or custom Docker environments) and a **Next.js 15 Frontend** (optimized for Vercel).

---

## Frontend Deployment (Next.js)

### Option 1: Vercel Dashboard (Recommended - Free & Easiest)

Vercel is the recommended hosting platform for Next.js applications, offering automatic builds and global CDN distribution.

1. **Push Code to GitHub**:
   Ensure your repository is pushed to GitHub:
   ```bash
   git remote add origin https://github.com/felixsutanto/multi-agent-research-system.git
   git branch -M main
   git push -u origin main
   ```

2. **Import to Vercel**:
   - Go to [vercel.com/new](https://vercel.com/new).
   - Sign in and import your repository: `felixsutanto/multi-agent-research-system`.

3. **Configure Project Settings**:
   Vercel will auto-detect the Next.js setup. Ensure the following configurations are set:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `./` (since Next.js files are in the root)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

4. **Set Environment Variables** (Critical):
   Expand the **Environment Variables** section and add:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://felix2712-multi-agent-research.hf.space` (or your custom backend endpoint)
   - **Environment**: Select `Production`, `Preview`, and `Development`.

5. **Deploy**:
   - Click **Deploy**.
   - Wait 2–3 minutes for the build to complete.
   - Your frontend will be live at `https://multi-agent-research-system.vercel.app` (or similar auto-generated domain).

---

### Option 2: Vercel CLI (Command Line Alternative)

```bash
# Install Vercel CLI globally
npm i -g vercel

# Log in to your Vercel account
vercel login

# Initialize deployment configuration
vercel

# Link to existing project? No
# Project name: multi-agent-research-system
# Directory: ./
# Override settings? Yes (specify build command: npm run build, output: .next)

# Add environment variable
vercel env add NEXT_PUBLIC_API_URL production
# Input value: https://felix2712-multi-agent-research.hf.space

# Deploy to production
vercel --prod
```

---

## Backend Deployment (Python/FastAPI)

The backend is designed to run efficiently on Hugging Face Spaces (using a Docker setup) or on any cloud provider supporting Docker / Python.

### Hosting on Hugging Face Spaces

1. **Create a Space**:
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space).
   - Select **Docker** as the SDK (use `Blank` template).
   - Select the Space hardware (the free CPU basic tier is sufficient).

2. **Configure app.py**:
   You can run the FastAPI server directly inside Hugging Face Spaces by setting `app.py` as your entry point:
   ```python
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   import uvicorn
   from src.api.main import app as backend_app

   app = backend_app

   # Configure CORS to allow secure requests from your Vercel frontend URL
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://multi-agent-research-system.vercel.app", "http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=7860)
   ```

3. **Deploy via Git**:
   Push the backend codebase to the Hugging Face Space repository. Hugging Face will build the Docker container and start your API on port `7860`.

---

## Docker Deployment (Self-Hosting)

You can build and deploy the entire backend using Docker.

### 1. Build the Docker Image
Ensure you have the following `Dockerfile` in the root:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and source
COPY requirements.txt .
COPY app.py .
COPY src/ ./src/
COPY config/ ./config/

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["python", "app.py"]
```

### 2. Run the Container
```bash
# Build
docker build -t multi-agent-research-backend .

# Run
docker run -d -p 7860:7860 \
  -e GROQ_API_KEY="your_groq_key" \
  -e TAVILY_API_KEY="your_tavily_key" \
  multi-agent-research-backend
```

---

## Alternative Cloud Providers (Frontend)

### Netlify Deployment
1. Import repository on [Netlify](https://netlify.com).
2. Set Build Command: `npm run build` and Publish Directory: `.next`.
3. Add `NEXT_PUBLIC_API_URL` environment variable.
4. Deploy site.

### AWS Amplify Deployment
1. Connect repository to AWS Amplify Console.
2. Select build configuration and set:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - npm ci
       build:
         commands:
           - npm run build
     artifacts:
       baseDirectory: .next
       files:
         - '**/*'
     cache:
       paths:
         - node_modules/**/*
   ```
3. Add the `NEXT_PUBLIC_API_URL` environment variable in the dashboard.
4. Save and deploy.

---

## Environment Variables Reference

| Variable | Scope | Required | Purpose |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | Frontend | Yes | API Base URL (e.g., `https://felix2712-multi-agent-research.hf.space` or `http://localhost:7860`) |
| `GROQ_API_KEY` | Backend | Yes | API key for LLM agent reasoning. |
| `TAVILY_API_KEY` | Backend | Yes | API key for web search retrieval. |

---

## Post-Deployment Verification Checklist

After deploying the backend and frontend, verify the system stability using this checklist:

- [ ] **Home Page Loading**: Visit your Vercel domain and check that the landing page loads, including theme toggle and query presets.
- [ ] **API Connection**: Submit a simple research query. Open DevTools (F12) to verify requests successfully route to the backend server.
- [ ] **WebSocket Streaming**: Observe the research progress. The agent timeline should animate and update in real-time as tasks execute.
- [ ] **Report Generation**: Verify the final Markdown report is synthesized successfully.
- [ ] **PDF Export**: Click the export option on a generated report and ensure the PDF is generated and downloaded correctly.
- [ ] **Responsive Test**: Inspect the page layouts on a mobile screen to ensure layout responsiveness.

---

## Troubleshooting

### Issue: Build Fails on Vercel
* **Cause**: Node.js engine mismatch or caching issue.
* **Fix**: Ensure your `package.json` supports Node `>=18.0.0` or clear the Vercel cache and redeploy.

### Issue: WebSocket Connection Fails (`wss://...` failed)
* **Cause**: Backend is not configured for SSL or CORS origin blocks it.
* **Fix**: Verify `NEXT_PUBLIC_API_URL` starts with `https://` (Vercel enforces SSL, so HTTP backend endpoints won't load due to mixed content restrictions). Ensure CORS headers allow your Vercel domain.

### Issue: API Connection Fails / Empty Responses
* **Cause**: Missing API keys on the backend host.
* **Fix**: Verify `GROQ_API_KEY` and `TAVILY_API_KEY` are set correctly in the Hugging Face Space secrets or docker container environment.
