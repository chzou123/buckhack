import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler

# Load dataset
df = pd.read_csv("NONseasonticket.csv")

# Display first few rows
df.head()

# ------------------------------------------------------------------------------
# 🔹 VALUE PLAN (Affordable Tickets for Weekday Games)
# ------------------------------------------------------------------------------
df['Total_Weekday_Games'] = df['Weekday Games']  # Total number of weekday games attended

df['CostSensitivityIndex'] = df['SingleGameTickets'] / df['NumGamesAttend'].replace(0, np.nan)  
# % of total tickets purchased that were single-game tickets (budget-conscious)

df['AvgSpend'] = df['AvgSpend'].astype(str).str.replace(r'[$,]', '', regex=True)  # Remove dollar signs
df['AvgSpend'] = pd.to_numeric(df['AvgSpend'], errors='coerce')  # Convert to numeric
df['Spending_Category'] = pd.qcut(df['AvgSpend'], q=3, labels=['Low', 'Mid', 'High'])  
# Categorized spending level (Low, Mid, High)

df['AvgSpend_Weekday'] = df['AvgSpend'] / df['Weekday Games'].replace(0, np.nan)
df['AvgSpend_Weekend'] = df['AvgSpend'] / df['Weekend Games'].replace(0, np.nan)
df['Weekday_Weekend_Spend_Diff'] = df['AvgSpend_Weekend'] - df['AvgSpend_Weekday']
# Difference in spend between weekday vs. weekend games

# ------------------------------------------------------------------------------
# 🔹 MARQUEE OPPONENT PLAN (Fans Who Prioritize Big Games)
# ------------------------------------------------------------------------------
df['Weekend_Games_Ratio'] = df['Weekend Games'] / df['NumGamesAttend'].replace(0, np.nan)
# % of total games attended that were marquee matchups (weekend)

game_columns = ['A Games', 'B Games', 'C Games', 'D Games']
df['Total_Tickets_Purchased'] = df[game_columns].sum(axis=1)  
# Total number of tickets purchased

df['Most_Common_Game_Type'] = df[game_columns].idxmax(axis=1).str[0]  
# Most frequently attended game type (A, B, C, D)

df['Most_Common_Game_Ratio'] = df[game_columns].max(axis=1) / df['Total_Tickets_Purchased'].replace(0, np.nan)
# Ratio of most attended game type to total tickets purchased

df["Marquee_Game_Ratio"] = df["A Games"] / df["NumGamesAttend"]

# ------------------------------------------------------------------------------
# 🔹 WEEKEND PLAN (Fans Who Prefer Weekend Entertainment)
# ------------------------------------------------------------------------------
df['Total_Weekend_Games'] = df['Weekend Games']  # Total weekend games attended
df['Weekend_Game_Ratio'] = df['Weekend Games'] / df['NumGamesAttend'].replace(0, np.nan)  
# % of total games that were weekend games

# ------------------------------------------------------------------------------
# 🔹 PROMOTIONAL GIVEAWAY INCLUSIVE PLAN
# ------------------------------------------------------------------------------
df['Total_Promo_Games'] = df['Promotional Games']  # Total number of promotional giveaway games attended
df['Promo_Games_Ratio'] = df['Promotional Games'] / df['NumGamesAttend'].replace(0, np.nan)
# % of total games that were promotional giveaways

# ------------------------------------------------------------------------------
# 🔹 GENERAL FEATURES (Useful for All Plans)
# ------------------------------------------------------------------------------
df['SocialMediaEngagement'] = pd.to_numeric(df['SocialMediaEngagement'], errors='coerce')
df['BasketballPropensity'] = pd.to_numeric(df['BasketballPropensity'], errors='coerce')
# Ensure numeric format for social & basketball engagement

df['ArenaProximityFactor'] = 1 / df['DistanceToArena'].replace(0, np.nan)
# Higher value = closer to the arena

# ------------------------------------------------------------------------------
# 🔹 DISPLAY & SAVE FINAL DATASET
# ------------------------------------------------------------------------------
print(df.head())  # Display first few rows
df.to_csv("enhanced_NONseasonticketing_data.csv", index=False)