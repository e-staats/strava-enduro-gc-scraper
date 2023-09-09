import os
import json
from pathlib import Path

from data_parser import parse_data
from leaderboard import create_leaderboard
import typer
from typing_extensions import Annotated

# from data import DATA
from printer import print_results
from strava_scraper import StravaSegmentLeaderboardScraper
from my_secrets import create_environment_variables

app = typer.Typer()


@app.command()
def run(
    segment_list_file: Annotated[
        Path,
        typer.Option(
            "--segments",
            "-s",
            help="The filepath to the txt file with your segment IDs (one per line)",
        ),
    ] = None,
    use_cached_data: Annotated[
        bool,
        typer.Option(
            "--use-cache",
            "-c",
            help="Whether or not to use the saved off data. Useful for when you just need to re-parse the data.",
        ),
    ] = False,
    results_cache_filepath: Annotated[
        Path, typer.Option(help="Where to save off the data cache")
    ] = Path(".", "data_cache.txt"),
    do_not_cache: Annotated[
        bool,
        typer.Option(
            help="Set this to not cache the data from this run. Useful when you want to keep the last data cache."
        ),
    ] = False,
):
    if use_cached_data:
        results = get_cached_data(results_cache_filepath)
    else:
        if not segment_list_file:
            raise ValueError(
                "You must provide a filepath to a list of segments if you are not using cached data."
            )
        create_environment_variables()
        validate_env_vars()

        print("Collecting segments...")
        segments = collect_segments(segment_list_file)

        print("Starting scraper...")
        scraper = StravaSegmentLeaderboardScraper(segments)
        scraper.run_scraper()
        results = scraper.get_results()
        print(results)

        if not do_not_cache:
            print(f"Saving off results to {results_cache_filepath}")
            results_cache_filepath.write_text(json.dumps(results))

    print("Parsing results...")
    rider_results = parse_data(results)

    print("Creating leaderboard.")
    leaderboard = create_leaderboard(rider_results)

    print("Printing results to file! Check the /printouts directory.")
    print_results(leaderboard)


def validate_env_vars():
    if os.environ.get("MY_STRAVA_PASSWORD") and os.environ.get("MY_STRAVA_EMAIL"):
        return
    raise ValueError(
        "You need to set the MY_STRAVA_EMAIL and MY_STRAVA_PASSWORD environment variable."
    )


def collect_segments(filepath: Path) -> list[str]:
    segments: list[str] = []
    with filepath.open("r") as f:
        data = f.readlines()
    for line in data:
        segments.append(line.split("#")[0].strip())
    return segments


def get_cached_data(filepath: Path) -> dict:
    if not filepath.exists():
        raise FileNotFoundError(f"Could not find results file at {filepath}")
    try:
        results = json.loads(filepath.read_text())
    except Exception as e:
        print(f"Exception trying to load cached data from {filepath}: {e}")
    if not results:
        raise ValueError(
            "Found results cache file but no data was loaded. Check file contents and rerun scraper if necessary"
        )
    return results


if __name__ == "__main__":
    app()
