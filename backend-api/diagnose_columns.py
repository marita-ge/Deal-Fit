"""Diagnostic script to check column names in Excel files."""
import pandas as pd
import config

print("=" * 60)
print("DIAGNOSING EXCEL FILE COLUMNS")
print("=" * 60)
print()

# Check main investor file
print("1. MAIN INVESTOR FILE:")
print(f"   File: {config.DATA_FILE_PATH}")
print("-" * 60)
try:
    df = pd.read_excel(config.DATA_FILE_PATH)
    print(f"   Columns ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    print(f"\n   First row sample (first 5 columns):")
    if len(df) > 0:
        for col in df.columns[:5]:
            value = df.iloc[0][col]
            print(f"   {col}: {value}")
    print()
except Exception as e:
    print(f"   ERROR: {e}\n")

# Check contacts file
print("2. CONTACTS FILE:")
print(f"   File: {config.CONTACTS_FILE_PATH}")
print("-" * 60)
try:
    df = pd.read_excel(config.CONTACTS_FILE_PATH)
    print(f"   Columns ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    print(f"\n   First row sample (first 5 columns):")
    if len(df) > 0:
        for col in df.columns[:5]:
            value = df.iloc[0][col]
            print(f"   {col}: {value}")
    print()
except Exception as e:
    print(f"   ERROR: {e}\n")

# Check Pitchbook contacts file
print("3. PITCHBOOK CONTACTS FILE:")
print(f"   File: {config.PITCHBOOK_CONTACTS_FILE_PATH}")
print("-" * 60)
try:
    df = pd.read_excel(config.PITCHBOOK_CONTACTS_FILE_PATH)
    print(f"   Columns ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    print(f"\n   First row sample (first 5 columns):")
    if len(df) > 0:
        for col in df.columns[:5]:
            value = df.iloc[0][col]
            print(f"   {col}: {value}")
    print()
except Exception as e:
    print(f"   ERROR: {e}\n")

print("=" * 60)
print("ANALYSIS:")
print("=" * 60)
print("Look for columns that contain firm/company names in each file.")
print("The matching logic looks for columns with these terms:")
print("  - 'firm', 'company', 'organization', 'investor', 'fund', 'name'")
print()

