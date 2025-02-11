import pandas as pd

# Load the CSV files
file1 = "seasonticket.csv"
file2 = "sorted_prompt1accountlevel.csv"
output_file = "seasontickets.csv"

# Read the CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Find rows that are in df1 but not in df2
diff1 = df1.merge(df2, how='outer', indicator=True).query('_merge != "both"').drop('_merge', axis=1)

# Save the differences to a new CSV file
diff1.to_csv(output_file, index=False)

print(f"Differences saved to {output_file}")
