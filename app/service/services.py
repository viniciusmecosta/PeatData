from app.infrastructure.firebase_client import FirebaseClient
from app.core.settings import settings
from datetime import datetime, timedelta
from app.core.constants import DISTANCE_FULL,COMEDOURO_CAPACITY
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
        try:
            timestamp_str = record["timestamp"].rstrip('Z')
            record_date = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
            record_date = fortaleza_tz.localize(record_date)
        except ValueError:
            print(f"Invalid timestamp format: {record['timestamp']}")
            continue
        
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
        try:
            timestamp_str = record["timestamp"].rstrip('Z')
            record_date = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
            record_date = fortaleza_tz.localize(record_date)
        except ValueError:
            print(f"Invalid timestamp format: {record['timestamp']}")
            continue
        
        if record_date.date() == target_date.date():
            filtered.append({
                "count": count,
                "data": record["timestamp"],
                "temp": record["temperature"],
                "humi": record["humidity"]
            })
            count += 1
    return filtered

def get_distance_by_days(days: int):
    end_date = datetime.now(fortaleza_tz)
    start_date = end_date - timedelta(days=days)
    records = firebase_client.get_data("sensor_distance")
    
    filtered = []
    count = 0
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        try:
            timestamp_str = record["timestamp"].rstrip('Z')
            record_date = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
            record_date = fortaleza_tz.localize(record_date)
        except ValueError:
            print(f"Invalid timestamp format: {record['timestamp']}")
            continue
        
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
        try:
            timestamp_str = record["timestamp"].rstrip('Z')
            record_date = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S")
            record_date = fortaleza_tz.localize(record_date)
        except ValueError:
            print(f"Invalid timestamp format: {record['timestamp']}")
            continue
        
        if record_date.date() == target_date.date():
            filtered.append({
                "count": count,
                "data": record["timestamp"],
                "level": record["level"]
            })
            count += 1
    return filtered

def add_phone(name: str, number: str):
    firebase_client.add_phone(name, number)

def get_all_phones():
    return firebase_client.get_all_phones()

def add_email(name: str, email: str):
    firebase_client.add_email(name, email)

def get_all_emails():
    return firebase_client.get_all_emails()

def calculate_comedouro_level(distance: float) -> int:
    level = 100 - ((distance / (COMEDOURO_CAPACITY - DISTANCE_FULL)) * 100)
    return round(level)


