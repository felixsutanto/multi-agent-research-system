# Quick Start Deployment Guide

## Prerequisites
- Node.js 18+ installed
- Git installed  
- Vercel account (free tier works)
- Backend API URL (Hugging Face Spaces or localhost)

## Option 1: Deploy to Vercel (Recommended)

###1. Push to GitHub
```bash
cd frontend
git init
git add .
git commit -m "Initial commit: Multi-Agent Research Frontend"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - Framework: Next.js
   - Root Directory: `./` (or `frontend` if in monorepo)
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL` = Your backend URL
6. Click "Deploy"

### 3. Done! 🎉
Your app will be live at `https://your-project.vercel.app`

## Option 2: Local Production Build

```bash
# Build
npm run build

# Start production server
npm start
```

Visit `http://localhost:3000`

## Option 3: Docker Deployment

```bash
# Build image
docker build -t research-frontend .

# Run container
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://your-backend research-frontend
```

## Environment Variables

Create `.env.local` (not committed to git):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production, set in Vercel dashboard:
- Deployment Settings → Environment Variables

## Post-Deployment Checklist

- [ ] Test all pages load
- [ ] Verify API connection  
- [ ] Test WebSocket/SSE streaming
- [ ] Check mobile responsiveness
- [ ] Test theme toggle
- [ ] Test language switcher
- [ ] Verify PDF export works
- [ ] Test share functionality

## Troubleshooting

**Build fails**: Check Node version (need 18+)
**API errors**: Verify `NEXT_PUBLIC_API_URL` is set correctly
**WebSocket fails**: Check CORS settings on backend

## Custom Domain (Optional)

In Vercel:
1. Go to Project Settings → Domains
2. Add your domain
3. Configure DNS (Vercel provides instructions)

---

**Need help?** Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed guide.
