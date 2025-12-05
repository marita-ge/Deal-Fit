"""Test that contact information is properly sourced from contact files."""
from data_loader import get_investor_data

print("=" * 80)
print("TESTING CONTACT FILE SOURCING")
print("=" * 80)

profiles = get_investor_data()

# Find investors with contacts from contact files
contact_file_contacts = []
main_file_contacts = []

for profile in profiles:
    if "contacts" in profile.get("metadata", {}):
        contacts = profile["metadata"]["contacts"]
        firm_name = profile['metadata'].get('Account Name', 'Unknown')
        
        for contact in contacts:
            if 'email' in contact and contact['email']:
                source = contact.get('source', 'unknown')
                if source == 'contact_files':
                    contact_file_contacts.append({
                        'firm': firm_name,
                        'contact': contact
                    })
                elif source == 'main_file':
                    main_file_contacts.append({
                        'firm': firm_name,
                        'contact': contact
                    })

print(f"\nContacts from CONTACT FILES: {len(contact_file_contacts)}")
print(f"Contacts from MAIN FILE: {len(main_file_contacts)}")
print(f"Total contacts with emails: {len(contact_file_contacts) + len(main_file_contacts)}")

print("\n" + "=" * 80)
print("SAMPLE CONTACTS FROM CONTACT FILES:")
print("=" * 80)

for i, item in enumerate(contact_file_contacts[:5], 1):
    print(f"\n{i}. Firm: {item['firm']}")
    contact = item['contact']
    print(f"   Name: {contact.get('name', 'N/A')}")
    print(f"   Email: {contact.get('email', 'N/A')}")
    print(f"   Source File: {contact.get('source_file', 'N/A')}")
    print(f"   Background: {contact.get('background', 'N/A')[:100]}")

print("\n" + "=" * 80)
print("VERIFYING CONTACT INFORMATION IN PROFILE TEXT:")
print("=" * 80)

# Check a sample profile to see how contact info is formatted
sample_profile = None
for profile in profiles:
    if "contacts" in profile.get("metadata", {}):
        contacts = profile["metadata"]["contacts"]
        for contact in contacts:
            if contact.get('source') == 'contact_files' and 'email' in contact:
                sample_profile = profile
                break
    if sample_profile:
        break

if sample_profile:
    print(f"\nSample Firm: {sample_profile['metadata'].get('Account Name', 'Unknown')}")
    print("\nProfile text (showing contact section):")
    print("-" * 80)
    text = sample_profile['text']
    # Find and show the contact information section
    if "CONTACT INFORMATION" in text:
        start_idx = text.find("CONTACT INFORMATION")
        contact_section = text[start_idx:start_idx+500]
        print(contact_section)
    else:
        print("Contact information section not found in profile text")
        print("\nLast 300 characters of profile:")
        print(text[-300:])
else:
    print("\nNo sample profile with contact file contacts found")

print("\n" + "=" * 80)

