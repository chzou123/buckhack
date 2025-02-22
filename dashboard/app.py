import streamlit as st
from bucks_stats import get_bucks_points_since_birth
from user_data import get_user_stats

st.title("🏀 Milwaukee Bucks Fan Experience Dashboard")

# User input
user_name = st.text_input("Enter Your Name:")
birth_year = st.number_input("Enter Your Birth Year:", min_value=1900, max_value=2025, value=2000)

if st.button("Get Your Bucks Stats"):
    total_points = get_bucks_points_since_birth(birth_year)
    st.metric(label="Total Bucks Points Since Your Birth", value=f"{total_points:,}")

    user_data = get_user_stats(user_name)
    if user_data is not None:
        st.write(f"🎟️ Tickets Purchased: {user_data['tickets_purchased']}")
        st.write(f"🏆 Rewards Earned: {user_data['rewards_earned']}")
    else:
        st.write("No user data found. Try another name.")