import random
import string
from datetime import datetime
import pytz
from app.core.constants import DISTANCE_FULL, COMEDOURO_CAPACITY

fortaleza_tz = pytz.timezone("America/Fortaleza")
SIMPLE_NAMES = ["Ana", "Maria", "Jose", "Joao", "Pedro", "Sofia", "Lucas", "Isabela"]
DOMAINS = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]


def calculate_comedouro_level(level: float) -> float:
    if level < DISTANCE_FULL:
        return 100
    if level > COMEDOURO_CAPACITY:
        return 0
    return round(100 - ((level - DISTANCE_FULL) / (COMEDOURO_CAPACITY - DISTANCE_FULL) * 100))


def generate_random_name() -> str:
    return f"{random.choice(SIMPLE_NAMES)} {random.choice(SIMPLE_NAMES)}"


def generate_random_phone() -> int:
    return int(f"{random.randint(11, 99)}9{random.randint(10000000, 99999999)}")


def generate_random_email(name: str) -> str:
    username = f"{name.lower().replace(' ', '')}{random.randint(100, 999)}"
    return f"{username}@{random.choice(DOMAINS)}"
