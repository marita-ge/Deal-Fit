"""
FastAPI backend wrapper for Deal Fit investor matching system.
Connects Next.js frontend to Python backend logic.
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

# Add the Deal Fit directory to the path
# Try multiple possible paths
current_file = Path(__file__).resolve()
possible_paths = [
    current_file.parent.parent.parent.parent / "Deal Fit",  # From Landing Page/backend-api/api/main.py
    current_file.parent.parent.parent / "Deal Fit",  # Alternative structure
    Path.cwd().parent / "Deal Fit",  # From backend-api directory
]

deal_fit_path = None
for path in possible_paths:
    if path.exists() and (path / "rag_pipeline.py").exists():
        deal_fit_path = path
        break

if deal_fit_path is None:
    raise ImportError(
        f"Could not find Deal Fit directory. Tried: {[str(p) for p in possible_paths]}. "
        f"Please ensure the Deal Fit folder is accessible."
    )

sys.path.insert(0, str(deal_fit_path))
print(f"✓ Found Deal Fit directory at: {deal_fit_path}")

# Import your existing modules
from rag_pipeline import InvestorRAGPipeline
from pdf_loader import extract_text_from_pdf
import config

app = FastAPI(title="Deal Fit API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        # Add your production domain here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG pipeline instance (initialized on first request)
rag_pipeline: Optional[InvestorRAGPipeline] = None
current_pitch_deck_text: Optional[str] = None

def get_rag_pipeline():
    """Lazy initialization of RAG pipeline."""
    global rag_pipeline
    if rag_pipeline is None:
        print("Initializing RAG pipeline...")
        rag_pipeline = InvestorRAGPipeline()
        print("RAG pipeline initialized!")
    return rag_pipeline


class ChatRequest(BaseModel):
    query: str
    pitch_deck_text: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    query: str


class UploadResponse(BaseModel):
    id: str
    name: str
    uploaded_at: str
    text_content: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Deal Fit API is running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat query and return investor recommendations.
    
    Uses the RAG pipeline to:
    1. Search for relevant investors using vector search
    2. Analyze pitch deck if provided
    3. Generate AI-powered recommendations
    """
    try:
        pipeline = get_rag_pipeline()
        
        # Set pitch deck if provided
        if request.pitch_deck_text:
            pipeline.set_pitch_deck(request.pitch_deck_text)
        elif current_pitch_deck_text:
            pipeline.set_pitch_deck(current_pitch_deck_text)
        else:
            pipeline.set_pitch_deck(None)
        
        # Generate recommendation
        response_text = pipeline.generate_recommendation(request.query)
        
        return ChatResponse(
            response=response_text,
            query=request.query
        )
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendation: {str(e)}"
        )


@app.post("/api/upload", response_model=UploadResponse)
async def upload_pitch_deck(file: UploadFile = File(...)):
    """
    Upload and process a PDF pitch deck.
    
    Extracts text from the PDF and stores it for use in chat queries.
    """
    file_path = None
    try:
        # Validate file type
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read file content
        contents = await file.read()
        
        # Use /tmp directory for serverless compatibility (only writable location)
        file_id = str(uuid.uuid4())
        file_path = Path("/tmp") / f"{file_id}.pdf"
        
        # Write to temp file
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Extract text from PDF
        try:
            text_content = extract_text_from_pdf(str(file_path))
            
            # Store pitch deck text globally (in production, use a session/database)
            global current_pitch_deck_text
            current_pitch_deck_text = text_content
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error extracting text from PDF: {str(e)}"
            )
        finally:
            # Clean up temp file
            if file_path and file_path.exists():
                try:
                    file_path.unlink()
                except Exception:
                    pass  # Ignore cleanup errors
        
        return UploadResponse(
            id=file_id,
            name=file.filename,
            uploaded_at=datetime.now().isoformat(),
            text_content=text_content
        )
    
    except HTTPException:
        # Clean up on error
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except Exception:
                pass
        raise
    except Exception as e:
        # Clean up on error
        if file_path and file_path.exists():
            try:
                file_path.unlink()
            except Exception:
                pass
        print(f"Error in upload endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )


@app.get("/api/pitch-decks")
async def list_pitch_decks():
    """
    List available pitch decks.
    In a production system, this would list stored pitch decks.
    """
    return {
        "pitch_decks": [],
        "message": "Pitch deck listing not yet implemented"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
