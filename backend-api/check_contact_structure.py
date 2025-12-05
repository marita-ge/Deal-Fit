"""Check the actual structure of contact files."""
import pandas as pd
import config

print("=" * 80)
print("CHECKING CONTACT FILES STRUCTURE")
print("=" * 80)

# Check Contacts file
print("\n1. CONTACTS FILE (Investor DATA - Contacts (DFD).xlsx)")
print("-" * 80)
try:
    df1 = pd.read_excel(config.CONTACTS_FILE_PATH)
    print(f"Shape: {df1.shape[0]} rows x {df1.shape[1]} columns")
    print(f"\nColumns: {list(df1.columns)}")
    
    # Check for email-related columns
    email_cols = [col for col in df1.columns if 'email' in col.lower() or 'contact' in col.lower() or 'name' in col.lower()]
    print(f"\nColumns with 'email', 'contact', or 'name': {email_cols}")
    
    print("\nFirst 2 complete rows:")
    for i in range(min(2, len(df1))):
        print(f"\n--- Row {i+1} ---")
        for col in df1.columns:
            val = df1.iloc[i][col]
            if pd.notna(val):
                val_str = str(val)
                if len(val_str) > 150:
                    val_str = val_str[:150] + "..."
                print(f"  {col}: {val_str}")
            else:
                print(f"  {col}: [NaN]")
except Exception as e:
    print(f"ERROR: {e}")

# Check Pitchbook Contacts file
print("\n\n2. PITCHBOOK CONTACTS FILE (Investor DATA - Pitchbook Contacts.xlsx)")
print("-" * 80)
try:
    df2 = pd.read_excel(config.PITCHBOOK_CONTACTS_FILE_PATH)
    print(f"Shape: {df2.shape[0]} rows x {df2.shape[1]} columns")
    print(f"\nColumns: {list(df2.columns)}")
    
    # Check for email-related columns
    email_cols = [col for col in df2.columns if 'email' in col.lower() or 'contact' in col.lower() or 'name' in col.lower()]
    print(f"\nColumns with 'email', 'contact', or 'name': {email_cols}")
    
    print("\nFirst 2 complete rows:")
    for i in range(min(2, len(df2))):
        print(f"\n--- Row {i+1} ---")
        for col in df2.columns:
            val = df2.iloc[i][col]
            if pd.notna(val):
                val_str = str(val)
                if len(val_str) > 150:
                    val_str = val_str[:150] + "..."
                print(f"  {col}: {val_str}")
            else:
                print(f"  {col}: [NaN]")
except Exception as e:
    print(f"ERROR: {e}")

# Compare with main file
print("\n\n3. MAIN INVESTOR FILE (for comparison)")
print("-" * 80)
try:
    df_main = pd.read_excel(config.DATA_FILE_PATH)
    print(f"Shape: {df_main.shape[0]} rows x {df_main.shape[1]} columns")
    print(f"Columns: {list(df_main.columns)}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 80)

