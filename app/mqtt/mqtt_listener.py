import json
import logging
from app.core.mqtt_core import (
    MQTT_BROKER,
    MQTT_PASSWORD,
    MQTT_PORT,
    MQTT_TOPIC_LEVEL,
    MQTT_TOPIC_SENSOR,
    MQTT_USER,
)
import colorlog
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.service.sensor_data_service import SensorDataService
from app.service.level_service import LevelService


handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s:     %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
)

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def handle_temperature_humidity(payload):
    try:
        data = json.loads(payload)
        db: Session = SessionLocal()
        sensor_service = SensorDataService(db)
        sensor_data = sensor_service.handle_sensor_data(
            data["temperature"], data["humidity"]
        )
        logger.info(
            f"Sensor data saved: Temp={sensor_data.temp}, Humi={sensor_data.humi}, Date={sensor_data.date}"
        )
    except Exception as e:
        logger.error(f"Error saving sensor data: {e}")
    finally:
        db.close()


def handle_level(payload):
    try:
        data = json.loads(payload)
        db: Session = SessionLocal()
        level_service = LevelService(db)
        level_data = level_service.handle_level(data["level"])
        logger.info(
            f"Level data saved: Level={level_data.level}, Date={level_data.date}"
        )
    except Exception as e:
        logger.error(f"Error saving level data: {e}")
    finally:
        db.close()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC_SENSOR)
        client.subscribe(MQTT_TOPIC_LEVEL)
    else:
        logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")


def on_message(client, userdata, msg):
    logger.debug(f"Received message on topic {msg.topic}")
    if msg.topic == MQTT_TOPIC_SENSOR:
        handle_temperature_humidity(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_LEVEL:
        handle_level(msg.payload.decode())


def start_mqtt_listener():
    client = mqtt.Client()
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
