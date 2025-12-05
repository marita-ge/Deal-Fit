# Deployment Guide

Complete guide for deploying Deal Fit landing page to Vercel.

## Prerequisites

- GitHub account
- Vercel account (free tier works)
- Backend API deployed (Railway, Render, etc.)

## Frontend Deployment (Vercel)

### Step 1: Push to GitHub

1. Initialize git repository (if not already):
   ```bash
   cd "Landing Page"
   git init
   git add .
   git commit -m "Initial commit: Deal Fit landing page"
   ```

2. Create a new repository on GitHub

3. Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/investor-match-platform.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in

2. Click "Add New Project"

3. Import your GitHub repository

4. Configure project settings:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `./` (or leave default)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next` (auto-detected)
   - **Install Command**: `npm install`

5. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL (e.g., `https://your-api.railway.app`)
   - `NEXT_PUBLIC_CALENDLY_URL`: Your Calendly URL (optional)
   - `ANTHROPIC_API_KEY`: (Only if calling Claude directly, otherwise in backend)

6. Click "Deploy"

### Step 3: Verify Deployment

1. Wait for build to complete (~2-5 minutes)

2. Visit your Vercel URL (e.g., `https://investor-match-platform.vercel.app`)

3. Test the application:
   - Landing page loads
   - Chat interface works
   - File upload works
   - API calls succeed

## Backend Deployment

### Option 1: Railway (Recommended)

1. Go to [railway.app](https://railway.app)

2. Click "New Project" → "Deploy from GitHub repo"

3. Select your repository and choose the `backend-api` folder

4. Set environment variables:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - (Copy any other vars from Deal Fit `.env`)

5. Railway will auto-detect Python and install dependencies

6. Update start command (if needed):
   ```
   uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```

7. Get your Railway URL and update `NEXT_PUBLIC_API_URL` in Vercel

### Option 2: Render

1. Go to [render.com](https://render.com)

2. Create new "Web Service"

3. Connect GitHub repository

4. Configure:
   - **Root Directory**: `backend-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

5. Add environment variables

6. Deploy!

### Option 3: Keep Backend Local (Development Only)

For local testing, run:
```bash
cd backend-api
source venv/bin/activate
uvicorn api.main:app --reload --port 8000
```

Use a tunneling service like ngrok:
```bash
ngrok http 8000
```

Update `NEXT_PUBLIC_API_URL` in Vercel with the ngrok URL.

## Post-Deployment Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed and accessible
- [ ] Environment variables set in Vercel
- [ ] CORS configured in backend for Vercel domain
- [ ] Test landing page loads
- [ ] Test file upload works
- [ ] Test chat queries work
- [ ] Verify investor recommendations appear
- [ ] Check error handling works

## Troubleshooting

### Build Failures

- Check build logs in Vercel dashboard
- Verify all dependencies in `package.json`
- Ensure TypeScript types are correct

### API Connection Issues

- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running and accessible
- Verify CORS settings in backend
- Check browser console for errors

### PDF Upload Issues

- Verify backend has write permissions
- Check file size limits
- Ensure backend API is receiving files

### Environment Variables

- Variables starting with `NEXT_PUBLIC_` are exposed to browser
- Don't put secrets in `NEXT_PUBLIC_` variables
- Update environment variables in Vercel dashboard if changed

## Custom Domain

1. Go to Vercel project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Monitoring

- Use Vercel Analytics (free tier available)
- Monitor backend API logs
- Set up error tracking (Sentry, etc.)

## Updates

After making changes:

1. Commit and push to GitHub
2. Vercel will auto-deploy (if enabled)
3. Backend needs manual redeploy (or set up CI/CD)

## Support

For issues, check:
- Vercel deployment logs
- Backend API logs
- Browser console errors
- Network tab for API calls
