import os
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC_SENSOR = os.getenv("MQTT_TOPIC_SENSOR")
MQTT_TOPIC_LEVEL = os.getenv("MQTT_TOPIC_LEVEL")
