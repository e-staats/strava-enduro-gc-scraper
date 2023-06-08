import pandas as pd


def create_leaderboard(rider_results: dict) -> pd.DataFrame:
    segments = get_segment_names(next(iter(rider_results.values())))
    leaderboard_data = {key: [] for key in segments}
    leaderboard_data["rider_name"] = []
    leaderboard_data["total_time"] = []

    for rider, rider_result in rider_results.items():
        # only count people with results for all of the segments:
        if len(rider_result["segments"]) != len(segments):
            continue

        leaderboard_data["rider_name"].append(rider)
        leaderboard_data["total_time"].append(rider_result["total_time"])
        for segment, time in rider_result["segments"].items():
            leaderboard_data[segment].append(time)

    leaderboard = pd.DataFrame(leaderboard_data)
    return leaderboard


def get_segment_names(rider_result: dict) -> list[str]:
    return list(rider_result.get("segments", {}).keys())


def get_segment_times(rider_result: dict) -> list[str]:
    return list(rider_result.get("segments", {}).values())
