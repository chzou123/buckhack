import pandas as pd

# -----------------------------
# Step 1. Read the Seat-Level Data
# -----------------------------
seatlevel_file = "Prompt1SeatLevel.csv"  # Contains: Season, AccountNumber, Game, GameDate, GameTier, weekday/weekend game, Promotional game
df_seat = pd.read_csv(seatlevel_file)

# (Optional) Ensure proper datatypes (if needed)
# Here we assume GameDate is already in an acceptable format and the flags are numeric (0/1).
# If needed, you could convert the "weekday/weekend game" and "Promotional game" columns as follows:
# df_seat['weekday/weekend game'] = pd.to_numeric(df_seat['weekday/weekend game'], errors='coerce')
# df_seat['Promotional game'] = pd.to_numeric(df_seat['Promotional game'], errors='coerce')

# -----------------------------
# Step 2. Aggregate Data by Account (and Season)
# -----------------------------
# We will group by Season and AccountNumber and then compute various counts.
# For fields not present in the seat-level file, we’ll set default values (e.g., 0 or blank).

group_cols = ["Season", "AccountNumber"]

# Prepare a list to collect account-level records.
account_records = []

# Loop over each group (each account in a season)
for (season, account), group in df_seat.groupby(group_cols):
    rec = {}
    # Basic identifiers
    rec["Season"] = season
    rec["AccountNumber"] = account

    # Set these account-level fields to default values (or later update them as needed)
    rec["SingleGameTickets"] = 0
    rec["PartialPlanTickets"] = 0
    rec["GroupTickets"] = 0
    rec["STM"] = 0
    rec["AvgSpend"] = 0
    rec["FanSegment"] = ""  # could be left blank or set to a default string
    rec["DistanceToArena"] = 0
    rec["BasketballPropensity"] = 0
    rec["SocialMediaEngagement"] = 0

    # GamesAttended: (if you wish to record total games attended from seat-level, you could use the row count;
    # however, we also want to record the distinct games attended below in NumGamesAttend)
    # For this example, we will set GamesAttended equal to the distinct games attended.
    distinct_game_count = group["Game"].nunique()
    rec["GamesAttended"] = distinct_game_count
    rec["NumGamesAttend"] = distinct_game_count

    # Count games by GameTier (A, B, C, D)
    rec["A Games"] = (group["GameTier"] == "A").sum()
    rec["B Games"] = (group["GameTier"] == "B").sum()
    rec["C Games"] = (group["GameTier"] == "C").sum()
    rec["D Games"] = (group["GameTier"] == "D").sum()

    # Count by day type
    rec["Weekend Games"] = (group["weekday/weekend game"] == 1).sum()
    rec["Weekday Games"] = (group["weekday/weekend game"] == 0).sum()

    # Count by promotional status
    rec["Promotional Games"] = (group["Promotional game"] == 1).sum()
    rec["Non Promo Games"] = (group["Promotional game"] == 0).sum()

    # Now, for each tier (A, B, C, D) and each combination of day type and promo status:
    #   Day type: Weekend (1) or Weekday (0)
    #   Promo: 1 for Promotional, 0 for NonPromo
    tiers = ["A", "B", "C", "D"]
    for tier in tiers:
        # For Weekend + Promo
        col_name = f"{tier} + Weekend + Promo"
        rec[col_name] = ((group["GameTier"] == tier) &
                         (group["weekday/weekend game"] == 1) &
                         (group["Promotional game"] == 1)).sum()
        # For Weekend + nonPromo
        col_name = f"{tier} + Weekend + nonPromo"
        rec[col_name] = ((group["GameTier"] == tier) &
                         (group["weekday/weekend game"] == 1) &
                         (group["Promotional game"] == 0)).sum()
        # For Weekday + Promo
        col_name = f"{tier} + Weekday + Promo"
        rec[col_name] = ((group["GameTier"] == tier) &
                         (group["weekday/weekend game"] == 0) &
                         (group["Promotional game"] == 1)).sum()
        # For Weekday + nonPromo
        col_name = f"{tier} + Weekday + nonPromo"
        rec[col_name] = ((group["GameTier"] == tier) &
                         (group["weekday/weekend game"] == 0) &
                         (group["Promotional game"] == 0)).sum()

    # Append the account record
    account_records.append(rec)

# Create the aggregated DataFrame
df_account = pd.DataFrame(account_records)

# -----------------------------
# Step 3. Reorder Columns as Specified
# -----------------------------
# The desired final column order is:
col_order = [
    "Season", "AccountNumber", "SingleGameTickets", "PartialPlanTickets", "GroupTickets", "STM", "AvgSpend",
    "GamesAttended", "FanSegment", "DistanceToArena", "BasketballPropensity", "SocialMediaEngagement",
    "A Games", "B Games", "C Games", "D Games",
    "Weekend Games", "Weekday Games", "Promotional Games", "Non Promo Games",
    "A + Weekend + Promo", "A + Weekend + nonPromo", "A + Weekday + Promo", "A + Weekday + nonPromo",
    "B + Weekend + Promo", "B + Weekend + nonPromo", "B + Weekday + Promo", "B + Weekday + nonPromo",
    "C + Weekend + Promo", "C + Weekend + nonPromo", "C + Weekday + Promo", "C + Weekday + nonPromo",
    "D + Weekend + Promo", "D + Weekend + nonPromo", "D + Weekday + Promo", "D + Weekday + nonPromo",
    "NumGamesAttend"
]

# Some of these columns might have been created in the loop; ensure they exist:
for col in col_order:
    if col not in df_account.columns:
        df_account[col] = 0

df_account = df_account[col_order]

# -----------------------------
# Step 4. Write the Account-Level File
# -----------------------------
accountlevel_file = "Prompt1AccountLevel.csv"
df_account.to_csv(accountlevel_file, index=False)

print(f"Aggregated account-level data saved to {accountlevel_file}")
