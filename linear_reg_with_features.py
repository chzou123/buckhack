import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# Load dataset
df = pd.read_csv("enhanced_NONseasonticketing_data.csv")

# Ensure all numeric data is properly formatted
df = df.apply(pd.to_numeric, errors='coerce')

# ---- DEBUG: Check missing data before applying fixes ----
print("\n🔹 Initial dataset shape:", df.shape)
print("\n🔹 Missing values before filling NaNs:")
print(df.isna().sum())

# Fill missing values instead of dropping rows
df.fillna(0, inplace=True)

# ---- Define Purchase Indicators for Each Plan ----
df['ValuePlan_Purchase'] = (df['Total_Weekday_Games'] > 2).astype(int)  # More than 2 weekday games
df['MarqueePlan_Purchase'] = (df['A Games'] > 1).astype(int)  # More than 1 marquee game (A Games)
df['WeekendPlan_Purchase'] = (df['Total_Weekend_Games'] > 1).astype(int)  # More than 1 weekend game
df['PromoPlan_Purchase'] = (df['Total_Promo_Games'] > 1).astype(int)  # More than 1 promo game

# ---- DEBUG: Ensure targets contain non-zero values ----
print("\n🔹 Total purchase counts per plan:")
print(df[['ValuePlan_Purchase', 'MarqueePlan_Purchase', 'WeekendPlan_Purchase', 'PromoPlan_Purchase']].sum())

# Define target columns
target_columns = {
    "Value Plan": "ValuePlan_Purchase",
    "Marquee Opponent Plan": "MarqueePlan_Purchase",
    "Weekend Plan": "WeekendPlan_Purchase",
    "Promotional Giveaway Plan": "PromoPlan_Purchase"
}

# Define feature columns (relevant predictors)
feature_columns = [
    'Total_Weekday_Games', 'CostSensitivityIndex', 'Weekday_Weekend_Spend_Diff',
    'A Games', 'Most_Common_Game_Ratio', 'Total_Weekend_Games', 
    'Promo_Games_Ratio', 'ArenaProximityFactor', 'SocialMediaEngagement', 'BasketballPropensity'
]

# Store results
results = {}

for plan, target in target_columns.items():
    print(f"\n🔹 Checking data availability for: {plan} ({target})")
    
    # Check data availability
    print("Before filtering:", df.shape)
    print("Missing values per column:")
    print(df[[target] + feature_columns].isna().sum())

    # Filter dataset (drop only necessary NaNs)
    df_filtered = df.dropna(subset=[target] + feature_columns)
    
    # Ensure we have enough data after filtering
    if df_filtered.shape[0] == 0:
        print(f"⚠️ Skipping {plan} - Not enough data after filtering!")
        continue

    # Define X (features) and y (target variable)
    X = df_filtered[feature_columns]
    y = df_filtered[target]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Linear Regression Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate model performance
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    # Store model coefficients
    coefficients = pd.Series(model.coef_, index=X.columns)

    # Save results
    results[plan] = {
        "R-squared": r2,
        "Mean Absolute Error": mae,
        "Feature Importance": coefficients
    }

    print(f"\n🔹 {plan} Model Results:")
    print(f"R² Score: {r2:.4f}")
    print(f"Mean Absolute Error: {mae:.4f}")
    print("\nFeature Importance:")
    print(coefficients.sort_values(ascending=False))

# ---- Display Results Summary ----
for plan, result in results.items():
    print(f"\n🔹 {plan} Model Summary:")
    print(f"R² Score: {result['R-squared']:.4f}")
    print(f"Mean Absolute Error: {result['Mean Absolute Error']:.4f}")
    print("\nFeature Importance:")
    print(result["Feature Importance"].sort_values(ascending=False))
