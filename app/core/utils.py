from datetime import datetime, timedelta
import pytz

from app.core.constants import DISTANCE_FULL, COMEDOURO_CAPACITY

fortaleza_tz = pytz.timezone("America/Fortaleza")


def parse_timestamp(timestamp: str) -> datetime:
    try:
        timestamp_str = timestamp.rstrip("Z")
        record_date = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
        return fortaleza_tz.localize(record_date)
    except ValueError:
        print(f"Invalid timestamp format: {timestamp}")
        return None


def calculate_comedouro_level(level: float) -> float:
    if level < DISTANCE_FULL:
        return 100
    elif level > COMEDOURO_CAPACITY:
        return 0
    level = 100 - ((level - DISTANCE_FULL) / (COMEDOURO_CAPACITY - DISTANCE_FULL) * 100)
    return round(level)
