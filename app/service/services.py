import random

from app.infrastructure.firebase_client import FirebaseClient
from app.core.settings import settings
from datetime import datetime, timedelta
from app.core.constants import DISTANCE_FULL, COMEDOURO_CAPACITY, COMEDOURO_ID
import pytz

fortaleza_tz = pytz.timezone('America/Fortaleza')

firebase_client = FirebaseClient(
    api_key=settings.FIREBASE_API_KEY,
    firestore_url=settings.FIREBASE_URL
)

def handle_temperature_humidity(temperature: float, humidity: float):
    timestamp = datetime.now(fortaleza_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "fields": {
            "timestamp": {"stringValue": timestamp},
            "temperature": {"doubleValue": temperature},
            "humidity": {"doubleValue": humidity}
        }
    }
    firebase_client.send_data("sensor_data", data)

def handle_level(level: float):
    level = calculate_comedouro_level(level)
    timestamp = datetime.now(fortaleza_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "fields": {
            "timestamp": {"stringValue": timestamp},
            "level": {"doubleValue": level}
        }
    }
    firebase_client.send_data("sensor_distance", data)

def get_temperature_by_days(days: int):
    end_date = datetime.now(fortaleza_tz)
    start_date = end_date - timedelta(days=days)
    records = firebase_client.get_data("sensor_data")

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

def get_temperature_by_date(date: str):
    target_date = datetime.strptime(date, "%d%m%Y").replace(tzinfo=fortaleza_tz)
    records = firebase_client.get_data("sensor_data")

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

def get_last_n_temperature_records(n: int):
    records = firebase_client.get_data("sensor_data")
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

def get_temperature_last_n_avg(n: int):
    end_date = datetime.now(fortaleza_tz)
    start_date = end_date - timedelta(days=n)
    records = firebase_client.get_data("sensor_data")

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

def get_last_n_level_records(n: int):
    records = firebase_client.get_data("sensor_distance")
    sorted_records = sorted(records, key=lambda x: x["timestamp"], reverse=True)[:n]

    return [
        {
            "count": index,
            "date": record["timestamp"],
            "level": record["level"]
        }
        for index, record in enumerate(sorted_records)
    ]

def get_level_by_days(days: int):
    end_date = datetime.now(fortaleza_tz)
    start_date = end_date - timedelta(days=days)
    records = firebase_client.get_data("sensor_distance")

    filtered = []
    count = 0
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        record_date = parse_timestamp(record["timestamp"])

        if start_date <= record_date <= end_date:
            filtered.append({
                "count": count,
                "date": record["timestamp"],
                "level": record["level"]
            })
            count += 1
    return filtered

def get_level_by_date(date: str):
    target_date = datetime.strptime(date, "%d%m%Y").replace(tzinfo=fortaleza_tz)
    records = firebase_client.get_data("sensor_distance")

    filtered = []
    count = 0
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        record_date = parse_timestamp(record["timestamp"])

        if record_date.date() == target_date.date():
            filtered.append({
                "count": count,
                "date": record["timestamp"],
                "level": record["level"]
            })
            count += 1
    return filtered

def get_levels_last_n_avg(n: int):
    end_date = datetime.now(fortaleza_tz)
    start_date = end_date - timedelta(days=n)
    records = firebase_client.get_data("sensor_distance")

    filtered = []
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        record_date = parse_timestamp(record["timestamp"])
        level = record.get("level")

        if level is not None:
            if start_date <= record_date <= end_date:
                filtered.append({
                    "date": record["timestamp"],
                    "level": float(level),
                })

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
        avg_data.append({
            "count": len(avg_data),
            "date": date,
            "level": avg_level,
        })

    return avg_data


def calculate_comedouro_level(level: float) -> float:
    if level < DISTANCE_FULL:
        return 100
    elif level > COMEDOURO_CAPACITY:
        return 0
    level = 100 - ((level - DISTANCE_FULL) / (COMEDOURO_CAPACITY - DISTANCE_FULL) * 100)
    return round(level)

def add_phone(name: str, number: str):
    data = {
            "fields": {
                "name": {"stringValue": name},
                "number": {"stringValue": number},
                "comedouro": {"integerValue": COMEDOURO_ID}
            }
        }
    firebase_client.send_data("phone", data)

def get_all_phones():
    records = firebase_client.get_data("phone")
    return [
        {

            "name": record["name"],
            "number": record["number"],
            "comedouro": record["comedouro"]
        }
        for record in records
    ]

def add_email(name: str, email: str):
    data = {
            "fields": {
                "name": {"stringValue": name},
                "email": {"stringValue": email},
                "comedouro": {"integerValue": COMEDOURO_ID}
            }
        }
    firebase_client.send_data("email", data)

def get_all_emails():
    records = firebase_client.get_data("email")
    return [
        {

            "name": record["name"],
            "email": record["email"],
            "comedouro": record["comedouro"]
        }
        for record in records
    ]

def parse_timestamp(timestamp: str) -> datetime:
    try:
        timestamp_str = timestamp.rstrip('Z')
        record_date = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
        return fortaleza_tz.localize(record_date)
    except ValueError:
        print(f"Invalid timestamp format: {timestamp}")
        return None

def delete_all_sensor_data():
    return firebase_client.delete_all_documents("sensor_data")

def delete_all_sensor_distance():
    return firebase_client.delete_all_documents("sensor_distance")


def generate_sensor_data():
    end_date = datetime.now(fortaleza_tz)
    for i in range(31):
        date = end_date - timedelta(days=i)
        timestamp = date.strftime("%Y-%m-%dT%H:%M:%SZ")

        temperature = round(random.uniform(20, 38), 1)
        humidity = round(random.uniform(30, 85), 1)

        data = {
            "fields": {
                "timestamp": {"stringValue": timestamp},
                "temperature": {"doubleValue": temperature},
                "humidity": {"doubleValue": humidity}
            }
        }

        firebase_client.send_data("sensor_data", data)

def generate_distance_data():
    end_date = datetime.now(fortaleza_tz)
    for i in range(31):
        date = end_date - timedelta(days=i)
        timestamp = date.strftime("%Y-%m-%dT%H:%M:%SZ")

        level = round(random.uniform(2, 25), 1)
        level = calculate_comedouro_level(level)

        data = {
            "fields": {
                "timestamp": {"stringValue": timestamp},
                "level": {"doubleValue": level}
            }
        }

        firebase_client.send_data("sensor_distance", data)