from app.infrastructure.firebase_client import FirebaseClient
from app.core.settings import settings
from datetime import datetime, timedelta
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
    timestamp = datetime.now(fortaleza_tz).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = {
        "fields": {
            "timestamp": {"stringValue": timestamp},
            "distance": {"doubleValue": distance}
        }
    }
    firebase_client.send_data("sensor_distance", data)

def get_temperature_by_days(days: int):
    end_date = datetime.now(fortaleza_tz)
    start_date = end_date - timedelta(days=days)
    records = firebase_client.get_data("sensor_data")
    
    filtered = []
    count = 1
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        record_date = datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=fortaleza_tz)
        if start_date <= record_date <= end_date:
            filtered.append({
                "count": count,
                "data": record["timestamp"],
                "temp": record["temperature"]
            })
            count += 1
    return filtered

def get_temperature_by_date(date: str):
    target_date = datetime.strptime(date, "%d%m%Y").replace(tzinfo=fortaleza_tz)
    records = firebase_client.get_data("sensor_data")
    
    filtered = []
    count = 1
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        record_date = datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=fortaleza_tz)
        if record_date.date() == target_date.date():
            filtered.append({
                "count": count,
                "data": record["timestamp"],
                "temp": record["temperature"]
            })
            count += 1
    return filtered

def get_distance_by_days(days: int):
    end_date = datetime.now(fortaleza_tz)
    start_date = end_date - timedelta(days=days)
    records = firebase_client.get_data("sensor_distance")
    
    filtered = []
    count = 1
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        record_date = datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=fortaleza_tz)
        if start_date <= record_date <= end_date:
            filtered.append({
                "count": count,
                "data": record["timestamp"],
                "distance": record["distance"]
            })
            count += 1
    return filtered

def get_distance_by_date(date: str):
    target_date = datetime.strptime(date, "%d%m%Y").replace(tzinfo=fortaleza_tz)
    records = firebase_client.get_data("sensor_distance")
    
    filtered = []
    count = 1
    for record in sorted(records, key=lambda x: x["timestamp"], reverse=True):
        record_date = datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=fortaleza_tz)
        if record_date.date() == target_date.date():
            filtered.append({
                "count": count,
                "data": record["timestamp"],
                "distance": record["distance"]
            })
            count += 1
    return filtered