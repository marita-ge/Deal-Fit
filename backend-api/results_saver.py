"""Save query results to file."""
import json
import os
import re
from datetime import datetime
from typing import Optional, Tuple
import config


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """
    Sanitize text to create a valid filename.
    
    Args:
        text: Text to sanitize
        max_length: Maximum length of filename
        
    Returns:
        Sanitized filename string
    """
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r'[^\w\s-]', '', text)
    sanitized = re.sub(r'[-\s]+', '-', sanitized)
    sanitized = sanitized.strip('-')
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip('-')
    
    return sanitized or "query"


def create_markdown_filename(query: str, timestamp: datetime, markdown_dir: Optional[str] = None) -> str:
    """
    Create a markdown filename based on query and timestamp.
    
    Args:
        query: The user's query
        timestamp: Timestamp of the query
        markdown_dir: Directory to save markdown files (defaults to config)
        
    Returns:
        Full path to the markdown file
    """
    if markdown_dir is None:
        markdown_dir = config.MARKDOWN_RESULTS_DIR
    
    # Create directory if it doesn't exist
    if markdown_dir and not os.path.exists(markdown_dir):
        os.makedirs(markdown_dir, exist_ok=True)
    
    # Format timestamp for filename (YYYY-MM-DD_HH-MM-SS)
    timestamp_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    
    # Sanitize query for filename
    query_sanitized = sanitize_filename(query, max_length=40)
    
    # Create filename: YYYY-MM-DD_HH-MM-SS_query-text.md
    filename = f"{timestamp_str}_{query_sanitized}.md"
    
    return os.path.join(markdown_dir, filename) if markdown_dir else filename


def format_markdown(query: str, response: str, pitch_deck_name: Optional[str] = None, timestamp: Optional[datetime] = None) -> str:
    """
    Format query result as markdown.
    
    Args:
        query: The user's query
        response: The AI-generated response
        pitch_deck_name: Name of the pitch deck used (if any)
        timestamp: Timestamp of the query
        
    Returns:
        Formatted markdown string
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    # Format timestamp for display
    timestamp_display = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    markdown_parts = [
        "# Investor Recommendation Query",
        "",
        f"**Date:** {timestamp_display}",
        ""
    ]
    
    if pitch_deck_name:
        markdown_parts.append(f"**Pitch Deck:** {pitch_deck_name}")
        markdown_parts.append("")
    
    markdown_parts.extend([
        "## Query",
        "",
        query,
        "",
        "---",
        "",
        "## Response",
        "",
        response
    ])
    
    return "\n".join(markdown_parts)


def save_query_result(
    query: str,
    response: str,
    pitch_deck_name: Optional[str] = None,
    results_file: Optional[str] = None
) -> Tuple[str, str]:
    """
    Save a query result to both JSON and markdown files.
    
    Args:
        query: The user's query
        response: The AI-generated response
        pitch_deck_name: Name of the pitch deck used (if any)
        results_file: Path to JSON results file (defaults to config)
        
    Returns:
        Tuple of (json_file_path, markdown_file_path)
    """
    if results_file is None:
        results_file = config.RESULTS_FILE_PATH
    
    timestamp = datetime.now()
    
    # Create results directory if it doesn't exist
    results_dir = os.path.dirname(results_file)
    if results_dir and not os.path.exists(results_dir):
        os.makedirs(results_dir, exist_ok=True)
    
    # Load existing results if file exists
    results = []
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or empty, start fresh
            results = []
    
    # Create new result entry
    result_entry = {
        "timestamp": timestamp.isoformat(),
        "query": query,
        "response": response,
        "pitch_deck": pitch_deck_name
    }
    
    # Append new result
    results.append(result_entry)
    
    # Save updated JSON results
    try:
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    except IOError as e:
        raise IOError(f"Error saving results to {results_file}: {str(e)}")
    
    # Save markdown file
    markdown_content = format_markdown(query, response, pitch_deck_name, timestamp)
    markdown_file = create_markdown_filename(query, timestamp)
    
    try:
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    except IOError as e:
        raise IOError(f"Error saving markdown to {markdown_file}: {str(e)}")
    
    return results_file, markdown_file


def load_query_results(results_file: Optional[str] = None) -> list:
    """
    Load all saved query results.
    
    Args:
        results_file: Path to results file (defaults to config)
        
    Returns:
        List of result dictionaries
    """
    if results_file is None:
        results_file = config.RESULTS_FILE_PATH
    
    if not os.path.exists(results_file):
        return []
    
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def get_results_count(results_file: Optional[str] = None) -> int:
    """
    Get the number of saved query results.
    
    Args:
        results_file: Path to results file (defaults to config)
        
    Returns:
        Number of saved results
    """
    results = load_query_results(results_file)
    return len(results)


def convert_json_to_markdown(results_file: Optional[str] = None) -> int:
    """
    Convert all existing JSON results to individual markdown files.
    Useful for migrating existing results.
    
    Args:
        results_file: Path to JSON results file (defaults to config)
        
    Returns:
        Number of markdown files created
    """
    results = load_query_results(results_file)
    count = 0
    
    for result in results:
        try:
            timestamp = datetime.fromisoformat(result["timestamp"])
            query = result["query"]
            response = result["response"]
            pitch_deck = result.get("pitch_deck")
            
            # Format and save markdown
            markdown_content = format_markdown(query, response, pitch_deck, timestamp)
            markdown_file = create_markdown_filename(query, timestamp)
            
            # Only create if file doesn't already exist
            if not os.path.exists(markdown_file):
                with open(markdown_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                count += 1
        except Exception as e:
            # Skip errors for individual entries
            continue
    
    return count

