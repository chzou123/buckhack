from nba_api.stats.endpoints import teamgamelog
import pandas as pd

def get_bucks_points_since_birth(year_of_birth):
    """Fetch total Bucks points scored since the user's birth year."""
    bucks_team_id = 1610612749  # Milwaukee Bucks team ID
    total_points = 0

    for season in range(year_of_birth, 2025):  # Fetch from birth year to now
        gamelog = teamgamelog.TeamGameLog(team_id=bucks_team_id, season=str(season))
        games = gamelog.get_data_frames()[0]
        total_points += games["PTS"].sum()

    return total_points
