"""Test script to verify contact data loading and matching."""
import sys
from data_loader import load_contact_data, get_investor_data, normalize_firm_name

def test_contact_loading():
    """Test that contact files are loaded correctly."""
    print("=" * 60)
    print("Testing Contact Data Loading")
    print("=" * 60)
    print()
    
    # Load contact data
    print("Loading contact data from Excel files...")
    contacts_by_firm = load_contact_data()
    
    if not contacts_by_firm:
        print("⚠️  WARNING: No contacts loaded. Check if contact files exist.")
        print(f"   Expected files:")
        print(f"   - DATA/Investor DATA - Contacts (DFD).xlsx")
        print(f"   - DATA/Investor DATA - Pitchbook Contacts.xlsx")
        return False
    
    print(f"✓ Successfully loaded contacts for {len(contacts_by_firm)} firms")
    print()
    
    # Show sample of loaded contacts
    print("Sample of loaded contacts (first 3 firms):")
    print("-" * 60)
    for i, (firm_name, contacts) in enumerate(list(contacts_by_firm.items())[:3]):
        print(f"\nFirm: {firm_name}")
        print(f"  Number of contacts: {len(contacts)}")
        if contacts:
            print(f"  First contact fields: {list(contacts[0].keys())}")
    print()
    
    return True


def test_investor_contact_matching():
    """Test that contacts are matched to investors."""
    print("=" * 60)
    print("Testing Investor-Contact Matching")
    print("=" * 60)
    print()
    
    print("Loading investor data with contacts...")
    profiles = get_investor_data()
    
    print(f"✓ Loaded {len(profiles)} investor profiles")
    print()
    
    # Count how many investors have contacts
    investors_with_contacts = 0
    total_contacts = 0
    
    print("Checking which investors have contact information...")
    print("-" * 60)
    
    for profile in profiles:
        if "contacts" in profile.get("metadata", {}):
            contacts = profile["metadata"]["contacts"]
            if contacts:
                investors_with_contacts += 1
                total_contacts += len(contacts)
    
    print(f"✓ Investors with contacts: {investors_with_contacts} out of {len(profiles)}")
    print(f"✓ Total contacts matched: {total_contacts}")
    print()
    
    # Show examples of investors with contacts
    print("Sample investors with contact information:")
    print("-" * 60)
    shown = 0
    for profile in profiles:
        if "contacts" in profile.get("metadata", {}):
            contacts = profile["metadata"]["contacts"]
            if contacts and shown < 3:
                # Try to find firm name in metadata
                firm_name = "Unknown"
                for key in ["Firm Name", "Company", "Investor", "Name"]:
                    if key in profile["metadata"]:
                        firm_name = profile["metadata"][key]
                        break
                
                print(f"\nInvestor: {firm_name}")
                print(f"  Contacts: {len(contacts)}")
                for i, contact in enumerate(contacts[:2], 1):  # Show first 2 contacts
                    print(f"  Contact {i}:")
                    # Show key fields (name, email if available)
                    for key in contact.keys():
                        if any(term in key.lower() for term in ['name', 'email', 'title', 'role']):
                            print(f"    {key}: {contact[key]}")
                shown += 1
    
    print()
    return investors_with_contacts > 0


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CONTACT DATA INTEGRATION TEST")
    print("=" * 60)
    print()
    
    # Test 1: Contact loading
    contacts_loaded = test_contact_loading()
    print()
    
    # Test 2: Investor-contact matching
    if contacts_loaded:
        matching_works = test_investor_contact_matching()
        print()
        
        if matching_works:
            print("=" * 60)
            print("✓ ALL TESTS PASSED!")
            print("=" * 60)
            print("\nContact data is being loaded and matched correctly.")
            print("When you run queries, contact information will be included.")
        else:
            print("=" * 60)
            print("⚠️  WARNING: Contacts loaded but not matched to investors")
            print("=" * 60)
            print("\nThis might mean:")
            print("  - Firm names in contact files don't match investor firm names")
            print("  - Check that firm name columns are correctly identified")
    else:
        print("=" * 60)
        print("⚠️  CONTACT FILES NOT FOUND")
        print("=" * 60)
        print("\nPlease ensure the contact Excel files are in the DATA folder.")
    
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

