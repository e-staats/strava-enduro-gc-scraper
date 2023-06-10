import pandas as pd
import numpy
from pathlib import Path


def print_results(leaderboard: pd.DataFrame):
    leaderboard.to_csv("./printouts/overall.csv")
    for column in leaderboard:
        leaderboard.sort_values(by=column, ascending=True, inplace=True)
        output = [f"Sorted by {column}\n"]
        output.append(",".join([col for col in leaderboard]) + "\n")
        for row in leaderboard.index:
            output_row = []
            for c in leaderboard:
                value = leaderboard[c][row]
                if isinstance(value, numpy.int64):
                    output_row.append(format_time(value))
                else:
                    output_row.append(value)
            output.append(",".join(output_row) + "\n")
        with Path(".", "printouts", f"{column}.csv").open("w") as f:
            f.writelines(output)
    return


def format_time(seconds: int) -> str:
    hours = str(seconds // 3600).rjust(2, "0")
    minutes = str(seconds // 60).rjust(2, "0")
    sec = str(seconds % 60).rjust(2, "0")
    if hours == "00":
        return f"{minutes}:{sec}"
    return f"{hours}:{minutes}:{sec}"
