import pandas as pd

# File names (assumed to be in the same folder as this script)
seatlevel_file = "Prompt1SeatLevel.csv"
gamelevel_file = "Prompt1GameLevel.csv"

# Read the CSV files
df_seat = pd.read_csv(seatlevel_file)
df_game = pd.read_csv(gamelevel_file)

# ------------------------------
# Process the Seat-Level File
# ------------------------------

# Convert the GameDate column to datetime (adjust format if necessary)
df_seat['GameDate'] = pd.to_datetime(df_seat['GameDate'], errors='coerce')

# Create the new column "weekday/weekend game"
# dt.weekday: Monday=0, Tuesday=1, ..., Saturday=5, Sunday=6.
# Mark as 1 if Saturday (5) or Sunday (6), else 0.
df_seat['weekday/weekend game'] = df_seat['GameDate'].dt.weekday.apply(lambda x: 1 if x >= 5 else 0)

# ------------------------------
# Merge with Game-Level File
# ------------------------------

# Merge on the "Game" column.
# Note: Ensure that the values in the "Game" column match between files.
df_updated = pd.merge(df_seat, df_game, on="Game", how="left")

# ------------------------------
# Create the "Promotional game" Column
# ------------------------------

# The game-level "Giveaway" column may contain strings like "Bucket Cap", "Lunch Bag", etc.
# We want to mark a game as promotional (1) if there is any non-empty text.
df_updated['Promotional game'] = df_updated['Giveaway'].apply(
    lambda x: 1 if isinstance(x, str) and x.strip() != "" else 0
)

# (Optional) Drop the original "Giveaway" column if it's no longer needed
df_updated = df_updated.drop(columns=["Giveaway"])

# ------------------------------
# Save the Updated CSV
# ------------------------------

# Write the updated DataFrame back to the seat-level CSV file
df_updated.to_csv(seatlevel_file, index=False)

print(f"Updated {seatlevel_file} with new columns 'weekday/weekend game' and 'Promotional game'.")
