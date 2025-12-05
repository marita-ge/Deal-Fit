"""Main CLI interface for investor recommendation system."""
import sys
from rag_pipeline import InvestorRAGPipeline
from pdf_loader import list_pitch_decks, load_pitch_deck
from results_saver import save_query_result


def select_pitch_deck(rag_pipeline: InvestorRAGPipeline):
    """
    Interactive pitch deck selection.
    
    Args:
        rag_pipeline: The RAG pipeline instance
        
    Returns:
        Name of selected pitch deck (or None)
    """
    pitch_decks = list_pitch_decks()
    
    if not pitch_decks:
        print("No pitch decks found in the 'Pitch Decks' folder.")
        print("You can continue without a pitch deck, or add PDF files to the folder.\n")
        return None
    
    print("\nAvailable Pitch Decks:")
    for i, deck in enumerate(pitch_decks, 1):
        print(f"  {i}. {deck}")
    print(f"  {len(pitch_decks) + 1}. None (continue without pitch deck)")
    
    while True:
        try:
            choice = input(f"\nSelect a pitch deck (1-{len(pitch_decks) + 1}): ").strip()
            
            if not choice:
                continue
            
            choice_num = int(choice)
            
            if choice_num == len(pitch_decks) + 1:
                rag_pipeline.set_pitch_deck(None)
                print("No pitch deck selected. Continuing without pitch deck analysis.\n")
                return None
            
            if 1 <= choice_num <= len(pitch_decks):
                selected_deck = pitch_decks[choice_num - 1]
                print(f"\nLoading pitch deck: {selected_deck}...")
                
                try:
                    pitch_deck_text = load_pitch_deck(selected_deck)
                    rag_pipeline.set_pitch_deck(pitch_deck_text)
                    print(f"✓ Pitch deck loaded successfully!\n")
                    return selected_deck
                except Exception as e:
                    print(f"Error loading pitch deck: {str(e)}\n")
                    continue
            
            print(f"Please enter a number between 1 and {len(pitch_decks) + 1}.")
        
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n")
            return None


def main():
    """Main CLI loop."""
    print("=" * 60)
    print("Investor Recommendation System")
    print("=" * 60)
    print()
    
    try:
        # Initialize recommendation pipeline (loads data automatically)
        rag_pipeline = InvestorRAGPipeline()
        
        # Select pitch deck before starting queries
        current_pitch_deck = select_pitch_deck(rag_pipeline)
        
        print("System ready! Enter your queries below.")
        print("Type 'exit', 'quit', or 'q' to exit.")
        print("Type 'change-deck' or 'deck' to select a different pitch deck.\n")
        
        # Interactive loop
        while True:
            try:
                # Get user query
                query = input("Query: ").strip()
                
                # Check for exit commands
                if query.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye!")
                    break
                
                # Check for pitch deck change command
                if query.lower() in ['change-deck', 'deck', 'change deck']:
                    current_pitch_deck = select_pitch_deck(rag_pipeline)
                    continue
                
                if not query:
                    print("Please enter a query.\n")
                    continue
                
                # Generate recommendation
                print("\nGenerating recommendation...\n")
                response = rag_pipeline.generate_recommendation(query)
                
                # Save query result
                try:
                    json_file, markdown_file = save_query_result(query, response, current_pitch_deck)
                    print(f"✓ Query result saved to JSON and markdown files.")
                    print(f"  Markdown: {markdown_file}\n")
                except Exception as save_error:
                    print(f"Warning: Could not save result: {str(save_error)}\n")
                
                # Display response
                print("-" * 60)
                print(response)
                print("-" * 60)
                print()
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}\n")
    
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

