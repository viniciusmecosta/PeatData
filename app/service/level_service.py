from datetime import datetime, timedelta
import pytz

from app.core.utils import calculate_comedouro_level, parse_timestamp
from app.repository.firebase_repository import FirebaseRepository
from app.core.settings import settings


class LevelService:
    def __init__(self):
        self.repository = FirebaseRepository(
            api_key=settings.FIREBASE_API_KEY, firestore_url=settings.FIREBASE_URL
        )
        self.fortaleza_tz = pytz.timezone("America/Fortaleza")

    def handle_level(self, level: float):
        level = calculate_comedouro_level(level)
        timestamp = datetime.now(self.fortaleza_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "fields": {
                "timestamp": {"stringValue": timestamp},
                "level": {"doubleValue": level},
            }
        }
        self.repository.send_data("sensor_distance", data)

    def get_last_n_level_records(self, n: int):
        records = self.repository.get_data("sensor_distance")
        sorted_records = sorted(records, key=lambda x: x["timestamp"], reverse=True)[:n]

        return [
            {"count": index, "date": record["timestamp"], "level": record["level"]}
            for index, record in enumerate(sorted_records)
        ]

    def get_level_by_days(self, days: int):
        end_date = datetime.now(self.fortaleza_tz)
        start_date = end_date - timedelta(days=days)
        records = self.repository.get_data("sensor_distance")

        filtered = []
        count = 0
        for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
            record_date = parse_timestamp(record["timestamp"])

            if start_date <= record_date <= end_date:
                filtered.append(
                    {
                        "count": count,
                        "date": record["timestamp"],
                        "level": record["level"],
                    }
                )
                count += 1
        return filtered

    def get_level_by_date(self, date: str):
        target_date = datetime.strptime(date, "%d%m%Y").replace(
            tzinfo=self.fortaleza_tz
        )
        records = self.repository.get_data("sensor_distance")

        filtered = []
        count = 0
        for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
            record_date = parse_timestamp(record["timestamp"])

            if record_date.date() == target_date.date():
                filtered.append(
                    {
                        "count": count,
                        "date": record["timestamp"],
                        "level": record["level"],
                    }
                )
                count += 1
        return filtered

    def get_levels_last_n_avg(self, n: int):
        end_date = datetime.now(self.fortaleza_tz)
        start_date = end_date - timedelta(days=n)
        records = self.repository.get_data("sensor_distance")

        filtered = []
        for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
            record_date = parse_timestamp(record["timestamp"])
            level = record.get("level")

            if level is not None:
                if start_date <= record_date <= end_date:
                    filtered.append(
                        {
                            "date": record["timestamp"],
                            "level": float(level),
                        }
                    )

        daily_data = {}
        for entry in filtered:
            date_str = parse_timestamp(entry["date"]).strftime("%d/%m")
            if date_str not in daily_data:
                daily_data[date_str] = {"level_sum": 0, "count": 0}

            daily_data[date_str]["level_sum"] += entry["level"]
            daily_data[date_str]["count"] += 1

        avg_data = []
        for date, values in daily_data.items():
            avg_level = round(values["level_sum"] / values["count"], 1)
            avg_data.append(
                {
                    "count": len(avg_data),
                    "date": date,
                    "level": avg_level,
                }
            )

        return avg_data
