import pandas as pd

# Read the CSV file
df = pd.read_csv("AccountInfo.csv")

# Sort by AccountNumber in ascending order
df_sorted = df.sort_values(by="AccountNumber")

# Save the sorted DataFrame back to a CSV file
df_sorted.to_csv("AccountInfo_sorted.csv", index=False)

print("Sorting complete. Saved as 'AccountInfo_sorted.csv'.")
