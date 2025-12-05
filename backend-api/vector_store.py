"""Local vector database for investor data using ChromaDB.
Pre-processes Excel data once, stores embeddings locally, enables fast semantic search.
"""
import os
# Suppress HuggingFace tokenizers warning (ChromaDB uses HuggingFace tokenizers internally)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import chromadb
from chromadb.config import Settings
from typing import List, Dict
import json
from data_loader import get_investor_data


class InvestorVectorStore:
    """Vector database for investor search using embeddings."""
    
    def __init__(self, persist_directory: str = "vector_db"):
        """
        Initialize vector store. Creates embeddings if not exists.
        
        Args:
            persist_directory: Directory to store the vector database
        """
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="investors",
            metadata={"hnsw:space": "cosine"}
        )
        self._ensure_data_loaded()
    
    def _ensure_data_loaded(self):
        """Check if data is loaded, if not, load and embed."""
        count = self.collection.count()
        if count == 0:
            print("=" * 60)
            print("FIRST TIME SETUP: Processing Excel data and creating embeddings...")
            print("This is a one-time operation that may take 2-5 minutes.")
            print("=" * 60)
            self._load_and_embed_investors()
        else:
            print(f"✓ Loaded vector database with {count} investor embeddings (cached).\n")
    
    def _load_and_embed_investors(self):
        """Load investors from Excel and create embeddings."""
        print("Loading investor data from Excel files...")
        profiles = get_investor_data()
        print(f"Loaded {len(profiles)} investors. Creating embeddings...")
        
        # Create concise summaries for embeddings (not full profiles)
        documents = []
        metadatas = []
        ids = []
        
        for i, profile in enumerate(profiles):
            if (i + 1) % 100 == 0:
                print(f"  Processing investor {i + 1}/{len(profiles)}...")
            
            # Create concise summary for semantic search
            summary = self._create_concise_summary(profile)
            documents.append(summary)
            
            # Store full data in metadata (for retrieval)
            metadatas.append({
                "full_text": profile['text'],
                "investor_id": profile['id'],
                "json_data": json.dumps(profile['metadata'], default=str)  # default=str handles any non-serializable types
            })
            ids.append(profile['id'])
        
        print(f"  Adding {len(profiles)} investors to vector database...")
        
        # Add to collection in batches (ChromaDB auto-generates embeddings)
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_end = min(i + batch_size, len(documents))
            self.collection.add(
                documents=documents[i:batch_end],
                metadatas=metadatas[i:batch_end],
                ids=ids[i:batch_end]
            )
            if batch_end < len(documents):
                print(f"  Processed batch {i//batch_size + 1}...")
        
        print(f"✓ Successfully processed and embedded {len(profiles)} investors!")
        print("  Future queries will use cached embeddings (no re-processing needed).\n")
    
    def _create_concise_summary(self, profile: Dict) -> str:
        """Create a concise summary of investor for embedding/search."""
        metadata = profile.get('metadata', {})
        parts = []
        
        # Key fields only for semantic search
        if 'Account Name' in metadata:
            parts.append(f"Firm: {metadata['Account Name']}")
        if 'Investor Focus Area' in metadata:
            parts.append(f"Focus: {metadata['Investor Focus Area']}")
        if 'Investor Type' in metadata:
            parts.append(f"Type: {metadata['Investor Type']}")
        if 'Fund Type' in metadata:
            parts.append(f"Fund Type: {metadata['Fund Type']}")
        if 'Check Size' in metadata:
            parts.append(f"Check Size: {metadata['Check Size']}")
        if 'Stage' in metadata:
            parts.append(f"Stage: {metadata['Stage']}")
        
        # Add any additional key fields that might be useful
        key_fields = ['Geographic Focus', 'Industry Focus', 'Investment Thesis', 
                     'Portfolio Companies', 'Minimum Investment', 'Maximum Investment']
        for field in key_fields:
            if field in metadata and metadata[field]:
                value = str(metadata[field])[:200]  # Limit length
                parts.append(f"{field}: {value}")
        
        # Get contact summary
        contacts = metadata.get('contacts', [])
        if contacts:
            contact_names = [c.get('name', '') for c in contacts[:2] if c.get('name')]
            if contact_names:
                parts.append(f"Contacts: {', '.join(contact_names)}")
        
        return " | ".join(parts)
    
    def search(self, query: str, n_results: int = 10) -> List[Dict]:
        """
        Semantic search for investors.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of investor profiles with full data
        """
        total_count = self.collection.count()
        if total_count == 0:
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, total_count)
        )
        
        # Reconstruct full investor profiles
        investors = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i, investor_id in enumerate(results['ids'][0]):
                metadata = results['metadatas'][0][i]
                try:
                    investors.append({
                        'id': investor_id,
                        'text': metadata['full_text'],
                        'metadata': json.loads(metadata['json_data'])
                    })
                except Exception as e:
                    print(f"Warning: Error loading investor {investor_id}: {str(e)}")
                    continue
        
        return investors
    
    def get_full_profile(self, investor_id: str) -> Dict:
        """Get full investor profile by ID."""
        results = self.collection.get(ids=[investor_id])
        if results['metadatas']:
            metadata = results['metadatas'][0]
            return {
                'id': investor_id,
                'text': metadata['full_text'],
                'metadata': json.loads(metadata['json_data'])
            }
        return None

