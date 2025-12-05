# Deal Fit Backend API

FastAPI wrapper that connects the Next.js frontend to your existing Python backend.

## Setup

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Installation

1. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp ../Deal\ Fit/.env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

   Or create a `.env` file with:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

4. **Ensure Deal Fit directory is accessible**:
   The backend API automatically finds the "Deal Fit" directory at the same level.
   If your structure is different, update the path in `api/main.py`.

## Running the Server

### Development

```bash
uvicorn api.main:app --reload --port 8000
```

### Production

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `POST /api/chat`

Send a query to get investor recommendations.

**Request Body**:
```json
{
  "query": "Find investors for fintech startups",
  "pitch_deck_text": "Optional pitch deck text content"
}
```

**Response**:
```json
{
  "response": "AI-generated recommendation text...",
  "query": "Find investors for fintech startups"
}
```

### `POST /api/upload`

Upload a PDF pitch deck for analysis.

**Request**: `multipart/form-data` with `file` field

**Response**:
```json
{
  "id": "uuid-here",
  "name": "pitch-deck.pdf",
  "uploaded_at": "2025-01-01T12:00:00",
  "text_content": "Extracted text from PDF..."
}
```

### `GET /health`

Health check endpoint.

## Integration with Deal Fit

The backend API uses your existing Python modules:

- `rag_pipeline.py` - Investor recommendation engine
- `pdf_loader.py` - PDF text extraction
- `vector_store.py` - Semantic investor search
- `data_loader.py` - Excel data processing
- `config.py` - Configuration settings

## CORS Configuration

Update `allow_origins` in `api/main.py` to include your production domains:

```python
allow_origins=[
    "http://localhost:3000",
    "https://your-domain.vercel.app",
]
```

## Deployment

### Option 1: Railway

1. Connect your GitHub repository
2. Set environment variables
3. Deploy!

### Option 2: Render

1. Create a new Web Service
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables

### Option 3: AWS Lambda / Google Cloud Run

Use a serverless framework to deploy the FastAPI app.

## Troubleshooting

### Import Errors

- Ensure the "Deal Fit" directory is at the correct relative path
- Check that all dependencies are installed
- Verify Python path in `api/main.py`

### CORS Issues

- Add your frontend URL to `allow_origins` in CORS middleware
- Check browser console for specific CORS errors

### PDF Upload Issues

- Verify file size limits (default: handled by FastAPI)
- Check `uploads/` directory permissions
- Ensure PyPDF2 can read the PDF format

## Notes

- The backend maintains pitch deck state in memory (single instance)
- For production, consider using a session store or database
- Vector database is initialized on first request (may take a few seconds)

