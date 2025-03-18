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

def handle_distance(distance: float):
    level = calculate_comedouro_level(distance)
    timestamp = datetime.now(fortaleza_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "fields": {
            "timestamp": {"stringValue": timestamp},
            "level": {"integerValue": level}
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
                "data": record["timestamp"],
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
                "data": record["timestamp"],
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
            "data": record["timestamp"],
            "temp": record["temperature"],
            "humi": record["humidity"]
        }
        for index, record in enumerate(sorted_records)
    ]

def get_last_n_level_records(n: int):
    records = firebase_client.get_data("sensor_distance")
    sorted_records = sorted(records, key=lambda x: x["timestamp"], reverse=True)[:n]

    return [
        {
            "count": index,
            "data": record["timestamp"],
            "level": record["level"]
        }
        for index, record in enumerate(sorted_records)
    ]

def get_distance_by_days(days: int):
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
                "data": record["timestamp"],
                "level": record["level"]
            })
            count += 1
    return filtered

def get_distance_by_date(date: str):
    target_date = datetime.strptime(date, "%d%m%Y").replace(tzinfo=fortaleza_tz)
    records = firebase_client.get_data("sensor_distance")

    filtered = []
    count = 0
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        record_date = parse_timestamp(record["timestamp"])

        if record_date.date() == target_date.date():
            filtered.append({
                "count": count,
                "data": record["timestamp"],
                "level": record["level"]
            })
            count += 1
    return filtered

def calculate_comedouro_level(distance: float) -> int:
    level = 100 - ((distance / (COMEDOURO_CAPACITY - DISTANCE_FULL)) * 100)
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
