import pandas as pd

# File names (assumed to be in the same folder as this script)
account_info_file = "AccountInfo_sorted.csv"
account_level_file = "Prompt1AccountLevel.csv"

# Read the CSV files
df_info = pd.read_csv(account_info_file)
df_level = pd.read_csv(account_level_file)

# Set 'AccountNumber' as the index for both DataFrames.
# This makes it easy to align rows for updating.
df_info.set_index("AccountNumber", inplace=True)
df_level.set_index("AccountNumber", inplace=True)

# List of columns to copy over from the account-info file.
cols_to_update = [
    "SingleGameTickets", "PartialPlanTickets", "GroupTickets", "STM", "AvgSpend",
    "FanSegment", "DistanceToArena", "BasketballPropensity", "SocialMediaEngagement"
]

# Loop over the columns to update.
# For each account number present in the account-info file, update the corresponding value in df_level.
for col in cols_to_update:
    if col in df_info.columns:
        # Only update the rows (accounts) that exist in df_level.
        # This replaces the existing value in df_level with the value from df_info.
        df_level.loc[df_level.index.intersection(df_info.index), col] = df_info.loc[df_level.index.intersection(df_info.index), col]
    else:
        print(f"Warning: Column '{col}' not found in {account_info_file}")

# (Optional) If you want to keep AccountNumber as a column rather than an index, reset the index.
df_level.reset_index(inplace=True)

# Write the updated DataFrame back to Prompt1AccountLevel.csv
df_level.to_csv(account_level_file, index=False)

print(f"Data from {account_info_file} has been copied over to {account_level_file} for the specified columns.")
