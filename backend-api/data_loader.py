"""Load and process investor data from Excel file."""
import pandas as pd
import re
from typing import List, Dict, Optional
import config


def load_investor_data(file_path: str = None) -> pd.DataFrame:
    """
    Load investor data from Excel file.
    
    Args:
        file_path: Path to Excel file. If None, uses config default.
        
    Returns:
        DataFrame with investor data
    """
    if file_path is None:
        file_path = config.DATA_FILE_PATH
    
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file not found at {file_path}")
    except Exception as e:
        raise Exception(f"Error reading Excel file: {str(e)}")


def load_contact_data(contacts_file: str = None, pitchbook_contacts_file: str = None) -> Dict[str, List[Dict]]:
    """
    Load contact data from Excel files and organize by firm name.
    
    Args:
        contacts_file: Path to contacts Excel file. If None, uses config default.
        pitchbook_contacts_file: Path to Pitchbook contacts Excel file. If None, uses config default.
        
    Returns:
        Dictionary mapping firm names to lists of contact dictionaries
    """
    contacts_by_firm = {}
    
    # Load contacts from both files
    contact_files = []
    if contacts_file is None:
        contacts_file = config.CONTACTS_FILE_PATH
    if pitchbook_contacts_file is None:
        pitchbook_contacts_file = config.PITCHBOOK_CONTACTS_FILE_PATH
    
    contact_files.append(contacts_file)
    contact_files.append(pitchbook_contacts_file)
    
    for file_path in contact_files:
        try:
            df = pd.read_excel(file_path)
            
            # Try to identify firm name column (common variations)
            # Prioritize "Account Name" or columns with "name" that aren't "Investor Notes"
            firm_col = None
            for col in df.columns:
                col_lower = str(col).lower()
                if 'account name' in col_lower or (col_lower == 'name' and 'note' not in col_lower):
                    firm_col = col
                    break
            
            # If not found, try other variations
            if firm_col is None:
                for col in df.columns:
                    col_lower = str(col).lower()
                    if any(term in col_lower for term in ['firm', 'company', 'organization']):
                        firm_col = col
                        break
            
            # If still not found, try first column
            if firm_col is None and len(df.columns) > 0:
                firm_col = df.columns[0]
            
            if firm_col is None:
                continue
            
            # Check if this file has structured contact person data (First Name, Last Name, Email columns)
            has_structured_contacts = any(col in df.columns for col in ['First Name', 'Email', 'Last Name'])
            
            # Group contacts by firm name
            for idx, row in df.iterrows():
                # Determine firm name - could be in "Company" column or firm_col
                firm_name = None
                if 'Company' in df.columns and pd.notna(row.get('Company')):
                    firm_name = str(row['Company']).strip()
                elif firm_col and pd.notna(row[firm_col]):
                    firm_name = str(row[firm_col]).strip()
                
                if not firm_name or firm_name.lower() in ['nan', 'none', '']:
                    continue
                
                # Normalize firm name for matching (lowercase, remove extra spaces)
                firm_name_normalized = firm_name.lower().strip()
                
                if firm_name_normalized not in contacts_by_firm:
                    contacts_by_firm[firm_name_normalized] = []
                
                # If file has structured contact person data (First Name, Email, etc.)
                if has_structured_contacts:
                    # Create structured contact from row
                    contact = {
                        'source': 'contact_files',
                        'source_file': 'Contacts (DFD)' if 'Contacts (DFD)' in file_path else 'Pitchbook Contacts'
                    }
                    
                    # Extract name
                    first_name = str(row.get('First Name', '')).strip() if pd.notna(row.get('First Name')) else ''
                    last_name = str(row.get('Last Name', '')).strip() if pd.notna(row.get('Last Name')) else ''
                    if first_name or last_name:
                        contact['name'] = f"{first_name} {last_name}".strip()
                    
                    # Extract email
                    if 'Email' in df.columns and pd.notna(row.get('Email')):
                        email = str(row['Email']).strip()
                        if email and '@' in email:
                            contact['email'] = email
                    
                    # Extract title/role
                    if 'Title' in df.columns and pd.notna(row.get('Title')):
                        contact['background'] = str(row['Title']).strip()
                    
                    # Only add if we have at least an email or name
                    if contact.get('email') or contact.get('name'):
                        # Add all other fields for context
                        for col in df.columns:
                            if col not in ['First Name', 'Last Name', 'Email', 'Title', 'Company']:
                                value = row[col]
                                if pd.notna(value) and str(value).strip():
                                    contact[col] = value
                        contacts_by_firm[firm_name_normalized].append(contact)
                
                else:
                    # Old format - extract from Notes field
                    notes_col = None
                    for col in df.columns:
                        if 'note' in col.lower():
                            notes_col = col
                            break
                    
                    extracted_contacts = []
                    if notes_col and pd.notna(row[notes_col]):
                        extracted_contacts = extract_contact_info_from_notes(row[notes_col])
                        
                        # Add each extracted contact
                        for contact in extracted_contacts:
                            # Mark source as contact file
                            contact['source'] = 'contact_files'
                            contact['source_file'] = 'Contacts (DFD)' if 'Contacts (DFD)' in file_path else 'Pitchbook Contacts'
                            contact['source_notes'] = str(row[notes_col])
                            contacts_by_firm[firm_name_normalized].append(contact)
                    
                    # Fallback: keep full row data if no structured contacts extracted
                    if not extracted_contacts:
                        full_contact = {}
                        for col in df.columns:
                            value = row[col]
                            if pd.notna(value) and str(value).strip():
                                full_contact[col] = value
                        if full_contact:
                            full_contact['source'] = 'contact_files'
                            full_contact['source_file'] = 'Contacts (DFD)' if 'Contacts (DFD)' in file_path else 'Pitchbook Contacts'
                            contacts_by_firm[firm_name_normalized].append(full_contact)
        
        except FileNotFoundError:
            # Continue if file doesn't exist
            continue
        except Exception as e:
            # Log error but continue
            print(f"Warning: Error loading contact file {file_path}: {str(e)}")
            continue
    
    return contacts_by_firm


def normalize_firm_name(name: str) -> str:
    """
    Normalize firm name for matching (lowercase, strip, remove common variations).
    
    Args:
        name: Firm name to normalize
        
    Returns:
        Normalized firm name
    """
    if pd.isna(name) or not name:
        return ""
    return str(name).lower().strip()


def extract_contact_info_from_notes(notes_text: str) -> List[Dict[str, str]]:
    """
    Extract structured contact information (name, email, background) from Investor Notes text.
    
    Args:
        notes_text: Text from Investor Notes field
        
    Returns:
        List of contact dictionaries with 'name', 'email', and 'background' fields
    """
    if pd.isna(notes_text) or not notes_text:
        return []
    
    notes_str = str(notes_text)
    contacts = []
    
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, notes_str)
    
    if not emails:
        return []
    
    # For each email, try to extract the associated name and context
    for email in emails:
        contact = {
            'email': email,
            'name': '',
            'background': ''
        }
        
        # Find the position of the email in the text
        email_pos = notes_str.find(email)
        
        # Extract text before email (likely contains name)
        before_email = notes_str[:email_pos].strip()
        
        # Try to extract name (look for patterns like "Name at Firm" or "Name, Title")
        # Common patterns: "John Doe at", "John Doe,", "John Doe -", "John Doe ("
        name_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+(?:at|,|-|\(|@)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+(?:at|,|-|\(|@)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+@',
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, before_email, re.IGNORECASE)
            if match:
                contact['name'] = match.group(1).strip()
                break
        
        # If no name found, try to get text right before email (last 30 chars)
        if not contact['name']:
            name_candidate = before_email[-50:].strip()
            # Remove common prefixes
            name_candidate = re.sub(r'^(at|from|contact|reach out to|email)\s+', '', name_candidate, flags=re.IGNORECASE)
            if name_candidate and len(name_candidate.split()) <= 4:
                contact['name'] = name_candidate
        
        # Extract text after email (likely contains background/context)
        after_email = notes_str[email_pos + len(email):].strip()
        # Get first 200 characters as background
        if after_email:
            contact['background'] = after_email[:200].strip()
            # Clean up background (remove extra spaces, newlines)
            contact['background'] = ' '.join(contact['background'].split())
        
        # Also try to get more context from before email
        if not contact['background'] and before_email:
            # Look for title/role information
            title_patterns = [
                r'(Principal|Partner|Director|Manager|Associate|Analyst|VP|Vice President|CEO|CTO|CFO)',
            ]
            for pattern in title_patterns:
                match = re.search(pattern, before_email, re.IGNORECASE)
                if match:
                    contact['background'] = match.group(1)
                    break
        
        contacts.append(contact)
    
    return contacts


def create_investor_profiles(df: pd.DataFrame, contacts_by_firm: Optional[Dict[str, List[Dict]]] = None) -> List[Dict[str, any]]:
    """
    Convert DataFrame rows to investor profile dictionaries with text representation.
    Includes contact information if available.
    
    Args:
        df: DataFrame with investor data
        contacts_by_firm: Dictionary mapping firm names to contact lists
        
    Returns:
        List of dictionaries, each containing investor data and text profile
    """
    profiles = []
    
    # Try to identify firm name column in investor data
    # Prioritize "Account Name" or columns with "name" that aren't "Investor Notes"
    firm_col = None
    for col in df.columns:
        col_lower = str(col).lower()
        if 'account name' in col_lower or (col_lower == 'name' and 'note' not in col_lower):
            firm_col = col
            break
    
    # If not found, try other variations
    if firm_col is None:
        for col in df.columns:
            col_lower = str(col).lower()
            if any(term in col_lower for term in ['firm', 'company', 'organization']):
                firm_col = col
                break
    
    # If still not found, try first column
    if firm_col is None and len(df.columns) > 0:
        firm_col = df.columns[0]
    
    for idx, row in df.iterrows():
        # Convert all non-null values to text representation
        profile_parts = []
        metadata = {}
        
        for col in df.columns:
            value = row[col]
            if pd.notna(value):
                # Store original value in metadata
                metadata[col] = value
                # Add to text profile
                profile_parts.append(f"{col}: {value}")
        
        # Try to match and add contact information from contact files
        contacts = []
        if contacts_by_firm and firm_col:
            firm_name = row[firm_col] if pd.notna(row[firm_col]) else None
            if firm_name:
                firm_name_normalized = normalize_firm_name(str(firm_name))
                # Try exact match first
                if firm_name_normalized in contacts_by_firm:
                    contacts = contacts_by_firm[firm_name_normalized]
                else:
                    # Try partial matching (in case of slight variations)
                    for contact_firm_name in contacts_by_firm.keys():
                        if firm_name_normalized in contact_firm_name or contact_firm_name in firm_name_normalized:
                            contacts = contacts_by_firm[contact_firm_name]
                            break
        
        # Also extract contacts from the main investor file's Notes field
        # This ensures we get contacts even if contact files don't have them
        notes_col = None
        for col in df.columns:
            if 'note' in col.lower():
                notes_col = col
                break
        
        if notes_col and pd.notna(row[notes_col]):
            main_file_contacts = extract_contact_info_from_notes(row[notes_col])
            # Merge with contacts from contact files (avoid duplicates)
            existing_emails = {c.get('email', '').lower() for c in contacts if 'email' in c}
            for contact in main_file_contacts:
                if contact.get('email', '').lower() not in existing_emails:
                    contact['source'] = 'main_file'
                    contacts.append(contact)
                    existing_emails.add(contact.get('email', '').lower())
        
        # Add contact information to profile - prioritize contact files
        if contacts:
            # Sort contacts: contact files first, then main file
            contacts_sorted = sorted(contacts, key=lambda x: (
                0 if x.get('source') == 'contact_files' else 1,
                x.get('source_file', '')
            ))
            
            profile_parts.append("\n=== CONTACT INFORMATION (from Contact Files) ===")
            contact_count = 0
            for contact in contacts_sorted:
                # Only show structured contacts (with email) prominently
                if 'email' in contact and contact['email']:
                    contact_count += 1
                    profile_parts.append(f"\nContact Person {contact_count}:")
                    
                    # Prioritize structured contact fields (name, email, background)
                    if 'name' in contact and contact['name']:
                        profile_parts.append(f"  Name: {contact['name']}")
                    if 'email' in contact and contact['email']:
                        profile_parts.append(f"  Email: {contact['email']}")
                    if 'background' in contact and contact['background']:
                        profile_parts.append(f"  Background/Role: {contact['background']}")
                    
                    # Show source file if from contact files
                    if contact.get('source') == 'contact_files':
                        profile_parts.append(f"  Source: {contact.get('source_file', 'Contact Files')}")
            
            # If no structured contacts but we have contact data, show it
            if contact_count == 0:
                profile_parts.append("\n(Contact information available in Notes field)")
            
            # Store all contacts in metadata (including non-structured ones)
            metadata["contacts"] = contacts_sorted
            metadata["contact_count"] = contact_count
        
        # Create full text profile
        text_profile = "\n".join(profile_parts)
        
        profiles.append({
            "id": str(idx),
            "text": text_profile,
            "metadata": metadata
        })
    
    return profiles


def get_investor_data() -> List[Dict[str, any]]:
    """
    Main function to load and process investor data.
    Also loads and merges contact information.
    
    Returns:
        List of investor profiles with contact information
    """
    df = load_investor_data()
    contacts_by_firm = load_contact_data()
    profiles = create_investor_profiles(df, contacts_by_firm)
    return profiles


def search_investors(profiles: List[Dict[str, any]], query: str, max_results: int = None) -> List[Dict[str, any]]:
    """
    Search through ALL investor profiles with improved scoring, then return top matches.
    This searches the entire database but only returns the most relevant ones.
    
    Args:
        profiles: List of investor profile dictionaries
        query: Search query string
        max_results: Maximum number of results to return (None = uses config default)
        
    Returns:
        List of top matching investor profiles
    """
    total_profiles = len(profiles)
    
    # Default to config limit if not specified
    if max_results is None:
        max_results = config.MAX_INVESTORS_TO_CLAUDE
    
    print(f"Searching ALL {total_profiles} investors in database...")
    
    query_lower = query.lower().strip()
    query_words = [w.strip() for w in query_lower.split() if len(w.strip()) > 2]
    
    # Score ALL profiles based on keyword matches with improved algorithm
    scored_profiles = []
    for profile in profiles:
        profile_text_lower = profile["text"].lower()
        score = 0
        
        # 1. Exact phrase match (highest priority - 200 points)
        if query_lower in profile_text_lower:
            score += 200
        
        # 2. All query words present (high priority - 150 points)
        all_words_present = all(word in profile_text_lower for word in query_words)
        if all_words_present and query_words:
            score += 150
        
        # 3. Individual word matches (weighted by frequency)
        for word in query_words:
            count = profile_text_lower.count(word)
            if count > 0:
                # More occurrences = higher score
                score += count * 15
        
        # 4. Check important fields for matches (boost score)
        metadata = profile.get("metadata", {})
        
        # Check Account Name
        if "Account Name" in metadata:
            account_name_lower = str(metadata["Account Name"]).lower()
            if query_lower in account_name_lower:
                score += 50
            for word in query_words:
                if word in account_name_lower:
                    score += 20
        
        # Check Investor Focus Area
        if "Investor Focus Area" in metadata:
            focus_area = str(metadata["Investor Focus Area"]).lower()
            for word in query_words:
                if word in focus_area:
                    score += 25
        
        # Check Investor Type
        if "Investor Type" in metadata:
            investor_type = str(metadata["Investor Type"]).lower()
            for word in query_words:
                if word in investor_type:
                    score += 20
        
        # Check Fund Type
        if "Fund Type" in metadata:
            fund_type = str(metadata["Fund Type"]).lower()
            for word in query_words:
                if word in fund_type:
                    score += 15
        
        # Always add profile with its score (even if 0)
        scored_profiles.append((score, profile))
    
    # Sort by score (highest first)
    scored_profiles.sort(key=lambda x: x[0], reverse=True)
    
    # Get top matches
    top_matches = [profile for _, profile in scored_profiles[:max_results]]
    
    # Count how many had matches
    matches_count = len([s for s, _ in scored_profiles if s > 0])
    
    print(f"Found {matches_count} investors with keyword matches.")
    print(f"Returning top {len(top_matches)} most relevant investors (top scores: {[s for s, _ in scored_profiles[:5]]})")
    
    return top_matches

