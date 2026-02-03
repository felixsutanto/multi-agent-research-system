# Vercel Deployment Configuration

## Project Structure

This repository contains:
- **Frontend**: Next.js app (root directory)
- **Backend**: Python FastAPI (`src/api/`)
- **Hugging Face**: Deployed separately on HF Spaces

## Vercel Settings

Use these settings when deploying to Vercel:

- **Framework**: Next.js (auto-detected)
- **Root Directory**: `./` (root directory)
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`
- **Node Version**: 18.x or higher

## Environment Variables

Add in Vercel Dashboard → Settings → Environment Variables:

```
NEXT_PUBLIC_API_URL=https://felix2712-multi-agent-research.hf.space
```

## Ignored Files

The `.vercelignore` file excludes:
- Python backend files
- Node modules
- Environment files
- Test files
- IDE configurations

## Deploy

```bash
# Via Vercel CLI
vercel

# Or via Vercel Dashboard
# Import from GitHub and use settings above
```

## Important Notes

- Frontend is in **root directory** (not in `/frontend` subfolder)
- Backend runs on Hugging Face Spaces (not deployed to Vercel)
- The`/frontend` subdirectory is the local development folder (ignore for Vercel)
