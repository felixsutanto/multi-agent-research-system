# Deployment Guide - Multi-Agent Research System Frontend

## 🚀 Deploying to Vercel (Recommended)

Vercel is the easiest and recommended platform for deploying Next.js applications.

### Prerequisites
- GitHub account
- Vercel account (free tier is sufficient)
- Code pushed to GitHub repository

### Step-by-Step Instructions

#### 1. Prepare Your Repository

```bash
# Navigate to frontend directory
cd frontend

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "feat: complete Next.js frontend for Multi-Agent Research System"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/multi-agent-research-frontend.git
git branch -M main
git push -u origin main
```

#### 2. Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Vercel will auto-detect Next.js configuration

#### 3. Configure Environment Variables

In the Vercel project settings, add:

```
NEXT_PUBLIC_API_URL=https://your-backend-url.hf.space
```

**Important**: Replace `your-backend-url.hf.space` with your actual Hugging Face Spaces URL or backend API URL.

#### 4. Deploy

- Click **"Deploy"**
- Wait 2-3 minutes for build to complete
- Your app will be live at: `https://your-project.vercel.app`

#### 5. Custom Domain (Optional)

1. Go to **Project Settings** → **Domains**
2. Add your custom domain
3. Follow DNS configuration instructions
4. Wait for SSL certificate to provision (~1 hour)

### Automatic Deployments

Vercel automatically deploys:
- **Production**: Every push to `main` branch
- **Preview**: Every pull request

---

## 🐳 Docker Deployment

For self-hosting or deploying to cloud platforms.

### Create Dockerfile

```dockerfile
FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

RUN mkdir .next
RUN chown nextjs:nodejs .next

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

### Build and Run

```bash
# Build image
docker build -t multi-agent-research-frontend .

# Run container
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=https://your-backend.hf.space multi-agent-research-frontend
```

---

## ☁️ AWS Amplify Deployment

### Prerequisites
- AWS account
- GitHub repository

### Steps

1. Go to AWS Amplify Console
2. Click **"New app"** → **"Host web app"**
3. Connect your GitHub repository
4. Configure build settings:
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
5. Add environment variable: `NEXT_PUBLIC_API_URL`
6. Click **"Save and Deploy"**

---

## 🌐 Netlify Deployment

### Via Netlify UI

1. Go to [netlify.com](https://netlify.com)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect GitHub repository
4. Configure build settings:
   - Build command: `npm run build`
   - Publish directory: `.next`
5. Add environment variable: `NEXT_PUBLIC_API_URL`
6. Click **"Deploy site"**

### Via CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Initialize
netlify init

# Deploy
netlify deploy --prod
```

---

## 🔧 Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-backend.hf.space` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_DEBUG` | Enable debug mode | `false` |

---

## 🔒 Backend Configuration

### CORS Setup

Your backend must allow requests from your frontend domain.

**FastAPI Example**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "http://localhost:3000"  # For development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### WebSocket Configuration

Ensure your backend supports WebSocket connections:
- Hugging Face Spaces: WebSocket supported by default
- Other platforms: May need specific configuration

---

## 📊 Performance Optimization

### Before Deployment

1. **Run Production Build Locally**
   ```bash
   npm run build
   npm start
   ```

2. **Check Bundle Size**
   ```bash
   npm run build
   # Look for "First Load JS shared by all"
   # Should be < 500KB
   ```

3. **Run Lighthouse Audit**
   - Open DevTools → Lighthouse
   - Run audit on production build
   - Ensure scores > 90

### Post-Deployment

1. **Enable Caching**
   - Vercel automatically caches static assets
   - For other platforms, configure CDN

2. **Monitor Performance**
   - Use Vercel Analytics
   - Or integrate Google Analytics

3. **Set up Error Tracking**
   - Sentry
   - LogRocket
   - Bugsnag

---

## 🧪 Testing Deployment

### Checklist

- [ ] Landing page loads correctly
- [ ] Dark/light mode toggle works
- [ ] Research form submits successfully
- [ ] WebSocket connects to backend
- [ ] Real-time updates display
- [ ] Reports generate and display
- [ ] Responsive design works on mobile
- [ ] All links work correctly
- [ ] Error states display properly

### Test Scenarios

1. **Start Research**
   - Enter query
   - Submit form
   - Verify WebSocket connection
   - Check agent timeline updates
   - Confirm report streams in

2. **View History**
   - Navigate to /history
   - Verify sessions display
   - Test rerun functionality
   - Test delete functionality

3. **Theme Toggle**
   - Switch between light/dark
   - Verify all components respect theme
   - Check localStorage persistence

---

## 🐛 Troubleshooting

### Build Fails on Vercel

**Error**: `Module not found`
- **Solution**: Delete `node_modules` and `.next`, then `npm clean-install`

**Error**: `Type errors`
- **Solution**: Run `npm run type-check` locally and fix errors

### WebSocket Connection Failed

**Error**: `WebSocket connection to 'wss://...' failed`
- **Solution**: Check `NEXT_PUBLIC_API_URL` is correct
- **Solution**: Verify CORS settings on backend
- **Solution**: Check if backend supports WebSocket

### Slow Performance

**Issue**: Pages load slowly
- **Solution**: Check bundle size with `npm run build`
- **Solution**: Optimize images (use Next.js Image component)
- **Solution**: Enable caching on CDN

### Environment Variables Not Working

**Issue**: `NEXT_PUBLIC_API_URL` is undefined
- **Solution**: Restart Vercel deployment
- **Solution**: Ensure variable starts with `NEXT_PUBLIC_`
- **Solution**: Rebuild the project

---

## 📈 Monitoring

### Vercel Analytics

Enable in project settings for:
- Page views
- Performance metrics
- Real-time visitors

### Custom Monitoring

Add to `src/app/layout.tsx`:

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

---

## 🔐 Security

### Best Practices

1. **Never commit sensitive data**
   - Use `.env.local` for secrets
   - Add to `.gitignore`

2. **Use environment variables**
   - Store API keys in Vercel settings
   - Access via `process.env.NEXT_PUBLIC_*`

3. **Enable Content Security Policy**
   - Configure in `next.config.ts`

4. **Rate Limiting**
   - Implement on API routes
   - Use middleware

---

## 📞 Support

**Deployment Issues**:
- Vercel Support: https://vercel.com/support
- Next.js Discord: https://nextjs.org/discord

**Questions**:
- GitHub Issues
- Stack Overflow

---

**Happy Deploying! 🚀**
