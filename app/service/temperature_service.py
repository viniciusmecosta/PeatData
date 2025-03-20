from app.core.utils import parse_timestamp
from app.repository.firebase_repository import FirebaseRepository
from app.core.settings import settings
from datetime import datetime, timedelta
import pytz

class TemperatureService:
    def __init__(self):
        self.repository = FirebaseRepository(
            api_key=settings.FIREBASE_API_KEY,
            firestore_url=settings.FIREBASE_URL
        )
        self.fortaleza_tz = pytz.timezone('America/Fortaleza')

    def handle_temperature_humidity(self,temperature: float, humidity: float):
        timestamp = datetime.now(self.fortaleza_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
        data = {
            "fields": {
                "timestamp": {"stringValue": timestamp},
                "temperature": {"doubleValue": temperature},
                "humidity": {"doubleValue": humidity}
            }
        }
        self.repository.send_data("sensor_data", data)

    def get_temperature_by_days(self, days: int):
        end_date = datetime.now(self.fortaleza_tz)
        start_date = end_date - timedelta(days=days)
        records = self.repository.get_data("sensor_data")

        filtered = []
        count = 0
        for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
            record_date = parse_timestamp(record["timestamp"])
            if start_date <= record_date <= end_date:
                filtered.append({
                    "count": count,
                    "date": record["timestamp"],
                    "temp": record["temperature"],
                    "humi": record["humidity"]
                })
                count += 1
        return filtered

    def get_temperature_by_date(self, date: str):
        target_date = datetime.strptime(date, "%d%m%Y").replace(tzinfo=self.fortaleza_tz)
        records = self.repository.get_data("sensor_data")

        filtered = []
        count = 0
        for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
            record_date = parse_timestamp(record["timestamp"])

            if record_date.date() == target_date.date():
                filtered.append({
                    "count": count,
                    "date": record["timestamp"],
                    "temp": record["temperature"],
                    "humi": record["humidity"]
                })
                count += 1
        return filtered

    def get_last_n_temperature_records(self, n: int):
        records = self.repository.get_data("sensor_data")
        sorted_records = sorted(records, key=lambda x: x["timestamp"], reverse=True)[:n]

        return [
            {
                "count": index,
                "date": record["timestamp"],
                "temp": record["temperature"],
                "humi": record["humidity"]
            }
            for index, record in enumerate(sorted_records)
        ]

    def get_temperature_last_n_avg(self, n: int):
        end_date = datetime.now(self.fortaleza_tz)
        start_date = end_date - timedelta(days=n)
        records = self.repository.get_data("sensor_data")

        filtered = []
        for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
            record_date = parse_timestamp(record["timestamp"])
            if start_date <= record_date <= end_date:
                filtered.append({
                    "date": record["timestamp"],
                    "temp": record["temperature"],
                    "humi": record["humidity"]
                })

        daily_data = {}
        for entry in filtered:
            date_str = parse_timestamp(entry["date"]).strftime("%d/%m")
            if date_str not in daily_data:
                daily_data[date_str] = {"temp_sum": 0, "humi_sum": 0, "count": 0}

            daily_data[date_str]["temp_sum"] += entry["temp"]
            daily_data[date_str]["humi_sum"] += entry["humi"]
            daily_data[date_str]["count"] += 1

        avg_data = []
        for date, values in daily_data.items():
            avg_temp = round(values["temp_sum"] / values["count"], 1)
            avg_humi = round(values["humi_sum"] / values["count"], 1)
            avg_data.append({
                "count": len(avg_data),
                "date": date,
                "temp": avg_temp,
                "humi": avg_humi
            })

        return avg_data
