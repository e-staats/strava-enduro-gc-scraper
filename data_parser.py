import math
from typing import Optional


def parse_data(data: dict[str, list]) -> dict[str, dict]:
    """
    Output Schema:

    {
        rider_name: {
            total_time: int,
            segments: {
                name: int
            }
        }
    }
    """
    parsed_data: dict[str, dict] = {}
    for segment_name, results in data.items():
        for result in results:
            rider_name = result[1]
            if isinstance(result[6], float):
                time = result[7]
            else:
                time = result[6]
            if seconds := convert_time_to_seconds(time):
                if not parsed_data.get(rider_name):
                    parsed_data[rider_name] = {"segments": {}, "total_time": 0}
                parsed_data[rider_name]["segments"][segment_name] = seconds
                parsed_data[rider_name]["total_time"] += seconds
    return parsed_data


def convert_time_to_seconds(time: str) -> Optional[int]:
    if isinstance(time, float):
        t = str(math.floor(time))
    elif "s" in time:
        t = f"00:{time.split('s')[0]}"
    else:
        t = time
    normalized_time = f"00:{t}" if t.count(":") == 1 else t
    try:
        h, m, s = normalized_time.split(":")
        return int(h) * 3600 + int(m) * 60 + int(s)
    except Exception as e:
        print(f"Exception parsing time {time}: {e}")
        return None
