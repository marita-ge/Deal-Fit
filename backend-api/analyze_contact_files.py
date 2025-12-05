"""Analyze contact files to understand their structure."""
import pandas as pd
import config

print("=" * 80)
print("ANALYZING CONTACT FILES")
print("=" * 80)

# Load all three files
df_main = pd.read_excel(config.DATA_FILE_PATH)
df_contacts = pd.read_excel(config.CONTACTS_FILE_PATH)
df_pitchbook = pd.read_excel(config.PITCHBOOK_CONTACTS_FILE_PATH)

print("\n1. FILE COMPARISON")
print("-" * 80)
print(f"Main file: {len(df_main)} rows, {df_main['Account Name'].nunique()} unique firms")
print(f"Contacts file: {len(df_contacts)} rows, {df_contacts['Account Name'].nunique()} unique firms")
print(f"Pitchbook file: {len(df_pitchbook)} rows, {df_pitchbook['Account Name'].nunique()} unique firms")

# Check if Notes differ
print("\n2. CHECKING FOR DIFFERENCES IN NOTES")
print("-" * 80)

# Find firms that have emails in Notes
import re
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

firms_with_emails_main = set()
firms_with_emails_contacts = set()
firms_with_emails_pitchbook = set()

for idx, row in df_main.iterrows():
    notes = str(row['Investor Notes']) if pd.notna(row['Investor Notes']) else ''
    if re.search(email_pattern, notes):
        firms_with_emails_main.add(row['Account Name'])

for idx, row in df_contacts.iterrows():
    notes = str(row['Investor Notes']) if pd.notna(row['Investor Notes']) else ''
    if re.search(email_pattern, notes):
        firms_with_emails_contacts.add(row['Account Name'])

for idx, row in df_pitchbook.iterrows():
    notes = str(row['Investor Notes']) if pd.notna(row['Investor Notes']) else ''
    if re.search(email_pattern, notes):
        firms_with_emails_pitchbook.add(row['Account Name'])

print(f"Firms with emails in Main file: {len(firms_with_emails_main)}")
print(f"Firms with emails in Contacts file: {len(firms_with_emails_contacts)}")
print(f"Firms with emails in Pitchbook file: {len(firms_with_emails_pitchbook)}")

# Find firms that have emails in contact files but not in main
only_in_contacts = firms_with_emails_contacts - firms_with_emails_main
only_in_pitchbook = firms_with_emails_pitchbook - firms_with_emails_main
in_both_contact_files = firms_with_emails_contacts & firms_with_emails_pitchbook

print(f"\nFirms with emails ONLY in Contacts file: {len(only_in_contacts)}")
print(f"Firms with emails ONLY in Pitchbook file: {len(only_in_pitchbook)}")
print(f"Firms with emails in BOTH contact files: {len(in_both_contact_files)}")

# Show examples
print("\n3. EXAMPLE FIRMS WITH EMAILS IN CONTACT FILES")
print("-" * 80)
if only_in_contacts:
    print(f"\nExample from Contacts file (not in main):")
    firm = list(only_in_contacts)[0]
    row = df_contacts[df_contacts['Account Name'] == firm].iloc[0]
    notes = str(row['Investor Notes']) if pd.notna(row['Investor Notes']) else ''
    print(f"Firm: {firm}")
    print(f"Notes: {notes[:300]}")

if only_in_pitchbook:
    print(f"\nExample from Pitchbook file (not in main):")
    firm = list(only_in_pitchbook)[0]
    row = df_pitchbook[df_pitchbook['Account Name'] == firm].iloc[0]
    notes = str(row['Investor Notes']) if pd.notna(row['Investor Notes']) else ''
    print(f"Firm: {firm}")
    print(f"Notes: {notes[:300]}")

# Check if Notes are different between files for same firm
print("\n4. CHECKING IF NOTES DIFFER FOR SAME FIRM")
print("-" * 80)
different_count = 0
for firm in df_main['Account Name'].head(20):
    main_row = df_main[df_main['Account Name'] == firm]
    contacts_row = df_contacts[df_contacts['Account Name'] == firm]
    pitchbook_row = df_pitchbook[df_pitchbook['Account Name'] == firm]
    
    if len(main_row) > 0 and len(contacts_row) > 0:
        main_notes = str(main_row.iloc[0]['Investor Notes']) if pd.notna(main_row.iloc[0]['Investor Notes']) else ''
        contacts_notes = str(contacts_row.iloc[0]['Investor Notes']) if pd.notna(contacts_row.iloc[0]['Investor Notes']) else ''
        if main_notes != contacts_notes:
            different_count += 1
            if different_count <= 3:
                print(f"\nFirm: {firm}")
                print(f"Main Notes: {main_notes[:150]}")
                print(f"Contacts Notes: {contacts_notes[:150]}")

print(f"\nTotal firms with different Notes (first 20 checked): {different_count}")

