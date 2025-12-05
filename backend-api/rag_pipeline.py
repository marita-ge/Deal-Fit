"""Efficient recommendation pipeline using vector search + Claude API."""
from anthropic import Anthropic
from typing import List, Dict, Optional
import config
from vector_store import InvestorVectorStore  # NEW: Use vector store instead


class InvestorRAGPipeline:
    """Efficient pipeline using vector search + Claude."""
    
    def __init__(self, vector_store: InvestorVectorStore = None):
        """
        Initialize the recommendation pipeline.
        
        Args:
            vector_store: Vector store instance (creates new one if None)
        """
        self.anthropic_client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.vector_store = vector_store or InvestorVectorStore()
        self.current_pitch_deck: Optional[str] = None
    
    def set_pitch_deck(self, pitch_deck_text: Optional[str]):
        """
        Set the current pitch deck content to analyze.
        
        Args:
            pitch_deck_text: Text content of the pitch deck, or None to clear
        """
        self.current_pitch_deck = pitch_deck_text
    
    def _create_concise_context(self, investors: List[Dict]) -> str:
        """Create concise context from investors for Claude (reduces token usage)."""
        if not investors:
            return "No relevant investors found."
        
        context_parts = []
        for i, investor in enumerate(investors, 1):
            metadata = investor.get('metadata', {})
            
            summary_parts = [f"Investor {i}:"]
            
            # Add key information only
            if 'Account Name' in metadata:
                summary_parts.append(f"  Firm: {metadata['Account Name']}")
            if 'Investor Focus Area' in metadata:
                summary_parts.append(f"  Focus: {metadata['Investor Focus Area']}")
            if 'Investor Type' in metadata:
                summary_parts.append(f"  Type: {metadata['Investor Type']}")
            if 'Fund Type' in metadata:
                summary_parts.append(f"  Fund Type: {metadata['Fund Type']}")
            if 'Check Size' in metadata:
                summary_parts.append(f"  Check Size: {metadata['Check Size']}")
            if 'Stage' in metadata:
                summary_parts.append(f"  Stage: {metadata['Stage']}")
            if 'Geographic Focus' in metadata:
                summary_parts.append(f"  Geographic Focus: {metadata['Geographic Focus']}")
            if 'Industry Focus' in metadata:
                summary_parts.append(f"  Industry Focus: {metadata['Industry Focus']}")
            
            # Include contacts (important!)
            contacts = metadata.get('contacts', [])
            if contacts:
                summary_parts.append("  CONTACT INFORMATION (from Contact Files):")
                for contact in contacts[:3]:  # Max 3 contacts per investor
                    contact_parts = []
                    if contact.get('name'):
                        contact_parts.append(f"Name: {contact['name']}")
                    if contact.get('email'):
                        contact_parts.append(f"Email: {contact['email']}")
                    if contact.get('background'):
                        contact_parts.append(f"Role: {contact['background']}")
                    if contact_parts:
                        summary_parts.append(f"    - {' | '.join(contact_parts)}")
            
            # Add any additional relevant fields (limited length)
            additional_fields = ['Investment Thesis', 'Portfolio Companies', 
                               'Minimum Investment', 'Maximum Investment']
            for field in additional_fields:
                if field in metadata and metadata[field]:
                    value = str(metadata[field])
                    if len(value) > 150:
                        value = value[:150] + "..."
                    summary_parts.append(f"  {field}: {value}")
            
            context_parts.append("\n".join(summary_parts))
        
        return "\n".join(context_parts)
    
    def generate_recommendation(self, query: str, max_results: int = None) -> str:
        """
        Generate investor recommendation using vector search + Claude.
        
        Args:
            query: User query
            max_results: Maximum number of investors to send to Claude (None = uses config default)
            
        Returns:
            Recommendation response from Claude
        """
        # Use config default if not specified (now reduced to 10)
        if max_results is None:
            max_results = config.MAX_INVESTORS_TO_CLAUDE
        
        print(f"\nSearching investor database using semantic search...")
        print(f"Query: '{query}'")
        
        # Vector search finds most relevant investors (semantic matching)
        investors = self.vector_store.search(query, n_results=max_results)
        
        print(f"Found {len(investors)} most relevant investors. Sending to Claude for analysis...\n")
        
        if not investors:
            return "No relevant investors found in the database for your query. Please try different keywords or criteria."
        
        # Create concise context (reduces token usage by ~80%)
        context = self._create_concise_context(investors)
        
        # Create prompt for Claude
        system_prompt = """You are a helpful assistant that recommends investors based on user queries and pitch deck analysis. 
Analyze the provided pitch deck (if available) and investor information to provide clear, concise recommendations. 
When a pitch deck is provided, carefully analyze the business, industry, stage, funding needs, and other relevant details.
Match investors based on their focus areas, investment criteria, check sizes, and portfolio alignment with the pitch deck.
Focus on explaining why each investor is a good match based on both the pitch deck content and the user's requirements.

You have access to a comprehensive database of investors. Carefully analyze ALL provided investors to identify the best matches.
Rank them by relevance and explain the reasoning. Only recommend investors that are truly good matches - quality over quantity.

CRITICAL: For each recommended investor, you MUST include the contact information from the "CONTACT INFORMATION (from Contact Files)" section. 
This includes:
- Contact person's Name
- Email address
- Background/Role information
This contact information is extracted from the Investor DATA - Contacts (DFD) and Investor DATA - Pitchbook Contacts files 
and is essential for the user to reach out to the investors. Always display this contact information prominently for each recommended investor."""

        # Build user prompt with pitch deck if available
        user_prompt_parts = ["Based on the following query, recommend the most relevant investors from the provided list."]
        
        if self.current_pitch_deck:
            user_prompt_parts.append(f"\nPitch Deck Content:\n{self.current_pitch_deck}\n")
        
        user_prompt_parts.append(f"\nUser Query: {query}")
        user_prompt_parts.append(f"\nRelevant Investors:\n{context}")
        user_prompt_parts.append("""
Please provide:
1. A brief analysis of the pitch deck (if provided) and user's requirements
2. Recommended investors ranked by relevance
3. Explanation of why each investor is a good match based on the pitch deck and requirements
4. Key details about each recommended investor
5. For EACH recommended investor, you MUST include the contact information from the "CONTACT INFORMATION (from Contact Files)" section:
   - Contact person's Name
   - Email address  
   - Background/Role information
   Format this contact information clearly and prominently. If contact information is not available for an investor, state that clearly.""")
        
        user_prompt = "\n".join(user_prompt_parts)

        # Call Claude API
        try:
            message = self.anthropic_client.messages.create(
                model=config.ANTHROPIC_MODEL,
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Extract response text
            response_text = ""
            for content_block in message.content:
                if content_block.type == "text":
                    response_text += content_block.text
            
            return response_text
        
        except Exception as e:
            return f"Error generating recommendation: {str(e)}"

