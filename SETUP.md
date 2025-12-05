# Quick Setup Guide

Get your landing page up and running quickly!

## Quick Start

### 1. Install Frontend Dependencies

```bash
cd "Landing Page"
npm install
```

### 2. Set Up Environment Variables

Create `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CALENDLY_URL=your_calendly_url_optional
```

### 3. Set Up Backend API

```bash
cd backend-api
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt

# Copy environment variables from Deal Fit
cp ../Deal\ Fit/.env .env
# Edit .env and ensure ANTHROPIC_API_KEY is set
```

### 4. Start Backend Server

```bash
# In backend-api directory
uvicorn api.main:app --reload --port 8000
```

### 5. Start Frontend (New Terminal)

```bash
# In Landing Page directory
npm run dev
```

### 6. Open Browser

Visit [http://localhost:3000](http://localhost:3000)

## What You'll See

1. **Landing Page** (`/`) - Hero, features, how it works, CTA
2. **Chat Interface** (`/chat`) - Upload pitch deck and ask questions

## Troubleshooting

### Backend Connection Issues

- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS settings in backend

### PDF Upload Issues

- Check file size (max 10MB)
- Ensure PDF is not password-protected
- Verify backend has write permissions

### Module Import Errors

- Ensure "Deal Fit" directory is at correct path
- Check Python dependencies are installed
- Verify environment variables are set

## Next Steps

- Read [README.md](./README.md) for detailed documentation
- Read [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment instructions
- Customize components to match your brand

## Project Structure

```
Landing Page/
├── app/                 # Next.js app router
├── components/          # React components
├── lib/                 # Utilities and store
├── types/               # TypeScript types
├── backend-api/         # FastAPI backend wrapper
└── public/              # Static assets
```

Happy coding! 🚀

