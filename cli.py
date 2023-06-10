from strava_scraper import StravaSegmentLeaderboardScraper
from data_parser import parse_data
from leaderboard import create_leaderboard
from test import YEET
from printer import print_results

print("Starting scraper...")
scraper = StravaSegmentLeaderboardScraper(
    [
        "1577102",  # Pinnacle
        "34572845",  # Amacher Hollow
        "34572822",  # Hyde
        "1577093",  # Mounds Park Rd
        "995757",  # JG to Mt Horeb
    ]
)
scraper.run_scraper()
results = scraper.get_results()
print("Parsing results...")
rider_results = parse_data(results)
print("Creating internal leaderboard.")
leaderboard = create_leaderboard(rider_results)
print("Printing results to file! Check the /printouts directory.")
print_results(leaderboard)
