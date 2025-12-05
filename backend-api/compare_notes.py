"""Compare Investor Notes between files to see if contact files have different/additional info."""
import pandas as pd
import config

# Load all three files
df_main = pd.read_excel(config.DATA_FILE_PATH)
df_contacts = pd.read_excel(config.CONTACTS_FILE_PATH)
df_pitchbook = pd.read_excel(config.PITCHBOOK_CONTACTS_FILE_PATH)

print("=" * 80)
print("COMPARING INVESTOR NOTES BETWEEN FILES")
print("=" * 80)

# Check a few examples to see if Notes differ
print("\nChecking if Notes fields differ between files...\n")

sample_firms = ["3x5 Partners", "4WARD"]
for firm_name in sample_firms:
    print(f"\n{'='*80}")
    print(f"FIRM: {firm_name}")
    print('='*80)
    
    # Find in each file
    main_row = df_main[df_main['Account Name'] == firm_name]
    contacts_row = df_contacts[df_contacts['Account Name'] == firm_name]
    pitchbook_row = df_pitchbook[df_pitchbook['Account Name'] == firm_name]
    
    if len(main_row) > 0:
        main_notes = main_row.iloc[0]['Investor Notes'] if pd.notna(main_row.iloc[0]['Investor Notes']) else "[Empty]"
        print(f"\nMAIN FILE Notes:\n{main_notes[:500]}")
    
    if len(contacts_row) > 0:
        contacts_notes = contacts_row.iloc[0]['Investor Notes'] if pd.notna(contacts_row.iloc[0]['Investor Notes']) else "[Empty]"
        print(f"\nCONTACTS FILE Notes:\n{contacts_notes[:500]}")
        if len(contacts_row) > 0 and len(main_row) > 0:
            if str(contacts_notes) != str(main_notes):
                print("\n✓ DIFFERENT - Contacts file has different/additional info!")
            else:
                print("\n✗ SAME - No additional info in contacts file")
    
    if len(pitchbook_row) > 0:
        pitchbook_notes = pitchbook_row.iloc[0]['Investor Notes'] if pd.notna(pitchbook_row.iloc[0]['Investor Notes']) else "[Empty]"
        print(f"\nPITCHBOOK FILE Notes:\n{pitchbook_notes[:500]}")
        if len(pitchbook_row) > 0 and len(main_row) > 0:
            if str(pitchbook_notes) != str(main_notes):
                print("\n✓ DIFFERENT - Pitchbook file has different/additional info!")
            else:
                print("\n✗ SAME - No additional info in pitchbook file")

# Check how many have different notes
print("\n\n" + "="*80)
print("STATISTICS")
print("="*80)

different_contacts = 0
different_pitchbook = 0
has_email_in_contacts = 0
has_email_in_pitchbook = 0

for idx, row in df_main.iterrows():
    firm_name = row['Account Name']
    main_notes = str(row['Investor Notes']) if pd.notna(row['Investor Notes']) else ""
    
    # Check contacts file
    contacts_match = df_contacts[df_contacts['Account Name'] == firm_name]
    if len(contacts_match) > 0:
        contacts_notes = str(contacts_match.iloc[0]['Investor Notes']) if pd.notna(contacts_match.iloc[0]['Investor Notes']) else ""
        if contacts_notes != main_notes:
            different_contacts += 1
        if '@' in contacts_notes:
            has_email_in_contacts += 1
    
    # Check pitchbook file
    pitchbook_match = df_pitchbook[df_pitchbook['Account Name'] == firm_name]
    if len(pitchbook_match) > 0:
        pitchbook_notes = str(pitchbook_match.iloc[0]['Investor Notes']) if pd.notna(pitchbook_match.iloc[0]['Investor Notes']) else ""
        if pitchbook_notes != main_notes:
            different_pitchbook += 1
        if '@' in pitchbook_notes:
            has_email_in_pitchbook += 1

print(f"\nRows with different Notes in Contacts file: {different_contacts} / {len(df_main)}")
print(f"Rows with emails in Contacts file Notes: {has_email_in_contacts} / {len(df_main)}")
print(f"\nRows with different Notes in Pitchbook file: {different_pitchbook} / {len(df_main)}")
print(f"Rows with emails in Pitchbook file Notes: {has_email_in_pitchbook} / {len(df_main)}")

