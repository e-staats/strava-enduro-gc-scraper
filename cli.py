from strava_scraper import StravaSegmentLeaderboardScraper
from data_parser import parse_data
from leaderboard import create_leaderboard
from test import YEET

scraper = StravaSegmentLeaderboardScraper(["780534", "15054428"])

scraper.run_scraper()
results = scraper.get_results()
rider_results = parse_data(results)
leaderboard = create_leaderboard(rider_results)
print(leaderboard)
