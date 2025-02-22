import pandas as pd

ticket_data = {
    "user_id": [1, 2, 3],
    "name": ["John Doe", "Jane Smith", "Michael Johnson"],
    "tickets_purchased": [15, 20, 5],
    "rewards_earned": ["Signed Jersey", "VIP Pass", "None"],
}

df = pd.DataFrame(ticket_data)

def get_user_stats(user_name):
    """Fetch user engagement data based on their name."""
    user = df[df["name"] == user_name]
    if user.empty:
        return None
    return user.iloc[0]