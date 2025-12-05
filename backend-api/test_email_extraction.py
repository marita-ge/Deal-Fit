"""Test email and contact extraction."""
from data_loader import get_investor_data, extract_contact_info_from_notes

print("=" * 80)
print("TESTING EMAIL AND CONTACT EXTRACTION")
print("=" * 80)

# Test extraction function directly
print("\n1. Testing extraction from sample notes:")
print("-" * 80)
sample_notes = "Jake Pflaum at 3x5 Partners jpflaum@3x5partners.com Principal at 3x5 and on third fund"
contacts = extract_contact_info_from_notes(sample_notes)
print(f"Extracted {len(contacts)} contacts:")
for i, contact in enumerate(contacts, 1):
    print(f"\n  Contact {i}:")
    print(f"    Name: {contact.get('name', 'N/A')}")
    print(f"    Email: {contact.get('email', 'N/A')}")
    print(f"    Background: {contact.get('background', 'N/A')[:100]}")

# Test with actual data
print("\n\n2. Testing with actual investor data:")
print("-" * 80)
profiles = get_investor_data()

# Find investors with extracted contacts (structured format)
investors_with_emails = []
for profile in profiles:
    if "contacts" in profile.get("metadata", {}):
        contacts = profile["metadata"]["contacts"]
        for contact in contacts:
            if 'email' in contact and contact['email']:
                investors_with_emails.append({
                    'firm': profile['metadata'].get('Account Name', 'Unknown'),
                    'contact': contact
                })
                break  # Only count once per investor

print(f"\nFound {len(investors_with_emails)} investors with extracted email contacts")
print("\nSample investors with extracted emails:")
print("-" * 80)

for i, item in enumerate(investors_with_emails[:5], 1):
    print(f"\n{i}. Firm: {item['firm']}")
    contact = item['contact']
    print(f"   Name: {contact.get('name', 'N/A')}")
    print(f"   Email: {contact.get('email', 'N/A')}")
    print(f"   Background: {contact.get('background', 'N/A')[:150]}")

print("\n" + "=" * 80)
print(f"✓ Total investors with extracted emails: {len(investors_with_emails)}")
print("=" * 80)

