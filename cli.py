import json
from pathlib import Path

from data_parser import parse_data
from leaderboard import create_leaderboard

# from data import DATA
from printer import print_results
from strava_scraper import StravaSegmentLeaderboardScraper

print("Starting scraper...")
scraper = StravaSegmentLeaderboardScraper(
    [
        # "1577102",  # Pinnacle
        # "34572845",  # Amacher Hollow
        # "34572822",  # Hyde
        # "1577093",  # Mounds Park Rd
        # "995757",  # JG to Mt Horeb
        "7372811",
        "29684950",
    ]
)
scraper.run_scraper()
results = scraper.get_results()
print(results)
results_cache = Path(".", "data.py")
print(f"Saving off results to {results_cache}")
with results_cache.open("w") as f:
    f.write(f"DATA = {json.dumps(results)}")
print("Parsing results...")

rider_results = parse_data(results)
print("Creating internal leaderboard.")
leaderboard = create_leaderboard(rider_results)
print("Printing results to file! Check the /printouts directory.")
print_results(leaderboard)
