"""Simple keyword-based search for investors."""
from typing import List, Dict
import config
from data_loader import get_investor_data, search_investors


class SimpleInvestorSearch:
    """Simple text-based investor search without embeddings."""
    
    def __init__(self):
        """Initialize with investor data."""
        print("Loading investor data...")
        self.profiles = get_investor_data()
        print(f"Loaded {len(self.profiles)} investors.\n")
    
    def search(self, query: str, max_results: int = None) -> List[Dict[str, any]]:
        """
        Search for investors matching the query.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of matching investor profiles
        """
        return search_investors(self.profiles, query, max_results)

