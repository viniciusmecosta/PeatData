import random
import string
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


def generate_random_name():
    simple_names = ["Ana", "Maria", "Jose", "Joao", "Pedro", "Sofia", "Lucas", "Isabela"]
    return random.choice(simple_names) + " " + random.choice(simple_names)

def generate_random_phone():
    number = int(f"{random.randint(11, 99)}9{random.randint(10000000, 99999999)}")
    return number

def generate_random_email(name):
    username = name.lower() + ''.join(random.choice(string.digits) for _ in range(3))
    username = username.replace(" ", "")
    domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]
    domain = random.choice(domains)
    return f"{username}@{domain}"
