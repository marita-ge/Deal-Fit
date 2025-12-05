# Deal Fit - Investor Match Platform

AI-powered platform that matches startups with the perfect investors using pitch deck analysis and semantic search.

## 🚀 Features

- **AI-Powered Matching**: Uses Claude AI to analyze pitch decks and match with relevant investors
- **Pitch Deck Analysis**: Upload PDF pitch decks for intelligent investor recommendations
- **Semantic Search**: Vector database for finding investors based on industry, stage, and focus areas
- **Contact Information**: Get direct contact details for recommended investors
- **Real-time Chat**: Interactive chat interface for refining investor searches

## 📁 Project Structure

```
investor-match-platform/
├── app/
│   ├── page.tsx                    # Landing page
│   ├── chat/
│   │   └── page.tsx                # Chat interface (main app)
│   ├── api/
│   │   ├── chat/
│   │   │   └── route.ts            # Chat API endpoint
│   │   └── upload/
│   │       └── route.ts            # Deck upload endpoint
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── landing/
│   │   ├── Hero.tsx
│   │   ├── HowItWorks.tsx
│   │   ├── Features.tsx
│   │   └── CTA.tsx
│   ├── chat/
│   │   ├── ChatInterface.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── ChatInput.tsx
│   │   └── DeckUpload.tsx
│   └── ui/
│       ├── button.tsx
│       ├── card.tsx
│       └── input.tsx
├── lib/
│   ├── anthropic.ts               # Claude client
│   ├── utils.ts                   # Utility functions
│   └── store.ts                   # Zustand store
├── types/
│   └── index.ts                   # TypeScript types
└── public/
    └── images/
```

## 🛠️ Setup Instructions

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.9+ (for backend API)
- Access to Anthropic API key (Claude)

### Step 1: Install Frontend Dependencies

```bash
cd "Landing Page"
npm install
# or
yarn install
```

### Step 2: Set Up Environment Variables

Create a `.env.local` file in the root directory:

```env
# Anthropic API Key (from your Deal Fit backend)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Backend API URL (FastAPI server)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Calendly URL
NEXT_PUBLIC_CALENDLY_URL=your_calendly_url
```

### Step 3: Set Up Python Backend API

The backend API wraps your existing Python code. You have two options:

#### Option A: Use FastAPI Backend (Recommended)

1. Navigate to the `backend-api` folder
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (copy from Deal Fit):
   ```bash
   cp ../Deal\ Fit/.env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```
5. Start the FastAPI server:
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```

#### Option B: Direct Python Integration (Simpler for MVP)

The Next.js API routes can call Python scripts directly. See `app/api/chat/route.ts` for implementation.

### Step 4: Run Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🔌 Backend Integration

The platform connects to your existing "Deal Fit" Python backend. The backend provides:

- **RAG Pipeline**: `rag_pipeline.py` - Investor recommendation engine
- **PDF Processing**: `pdf_loader.py` - Pitch deck text extraction
- **Vector Store**: `vector_store.py` - Semantic investor search
- **Data Loading**: `data_loader.py` - Excel data processing

### API Endpoints

The FastAPI backend exposes these endpoints:

- `POST /api/chat` - Send query and get investor recommendations
- `POST /api/upload` - Upload and process pitch deck PDF
- `GET /api/pitch-decks` - List available pitch decks

## 🚢 Deployment

### Vercel Deployment

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard:
   - `ANTHROPIC_API_KEY`
   - `NEXT_PUBLIC_API_URL` (your FastAPI backend URL)
   - `NEXT_PUBLIC_CALENDLY_URL`

4. Deploy!

### Backend Deployment

Deploy the FastAPI backend to:
- Railway
- Render
- AWS Lambda
- Or keep it on a VPS

Update `NEXT_PUBLIC_API_URL` to point to your deployed backend.

## 🎨 Customization

### Calendly Integration

1. Get your Calendly URL
2. Add it to `.env.local` as `NEXT_PUBLIC_CALENDLY_URL`
3. The CalendlyButton component will use it automatically

### Styling

The project uses Tailwind CSS. Customize colors in `tailwind.config.js`:

```js
theme: {
  extend: {
    colors: {
      primary: '#your-color',
      // ...
    }
  }
}
```

## 📝 Development

### Adding New Features

- **Components**: Add to `components/` folder
- **API Routes**: Add to `app/api/` folder
- **Types**: Add to `types/index.ts`

### Testing

```bash
npm run test
```

## 🐛 Troubleshooting

### Backend Connection Issues

- Ensure FastAPI server is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS settings in FastAPI backend

### PDF Upload Issues

- Check file size limits (default: 10MB)
- Ensure PDF is not password-protected
- Verify backend has write permissions for uploads folder

## 📚 Documentation

For more details on the backend integration, see:
- `backend-api/README.md` - Backend API documentation
- `../Deal Fit/README.md` - Original CLI tool documentation

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

[Your License Here]

## 🆘 Support

For issues or questions, please open a GitHub issue.
