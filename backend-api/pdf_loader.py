"""Load and extract text from PDF pitch decks."""
import os
import PyPDF2
from typing import List, Optional
import config


def list_pitch_decks(folder_path: str = None) -> List[str]:
    """
    List all PDF files in the pitch decks folder.
    
    Args:
        folder_path: Path to pitch decks folder. If None, uses config default.
        
    Returns:
        List of PDF filenames
    """
    if folder_path is None:
        folder_path = config.PITCH_DECKS_FOLDER
    
    if not os.path.exists(folder_path):
        return []
    
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    return sorted(pdf_files)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Full path to the PDF file
        
    Returns:
        Extracted text content
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_parts = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_parts.append(f"--- Page {page_num + 1} ---\n{page_text}")
                except Exception as e:
                    # Skip pages that can't be read
                    continue
            
            return "\n\n".join(text_parts)
    
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    except Exception as e:
        raise Exception(f"Error reading PDF file {pdf_path}: {str(e)}")


def load_pitch_deck(filename: str, folder_path: str = None) -> str:
    """
    Load and extract text from a specific pitch deck PDF.
    
    Args:
        filename: Name of the PDF file
        folder_path: Path to pitch decks folder. If None, uses config default.
        
    Returns:
        Extracted text content
    """
    if folder_path is None:
        folder_path = config.PITCH_DECKS_FOLDER
    
    pdf_path = os.path.join(folder_path, filename)
    return extract_text_from_pdf(pdf_path)


def get_pitch_deck_path(filename: str, folder_path: str = None) -> str:
    """
    Get the full path to a pitch deck file.
    
    Args:
        filename: Name of the PDF file
        folder_path: Path to pitch decks folder. If None, uses config default.
        
    Returns:
        Full path to the PDF file
    """
    if folder_path is None:
        folder_path = config.PITCH_DECKS_FOLDER
    
    return os.path.join(folder_path, filename)

