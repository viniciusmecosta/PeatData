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
import paho.mqtt.client as paho
from paho import mqtt
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
    db = None
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
        if db is not None and db.is_active:
            db.close()


def handle_level(payload):
    db = None
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
        if db is not None and db.is_active:
            db.close()


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC_SENSOR, qos=2)
        client.subscribe(MQTT_TOPIC_LEVEL, qos=2)
    else:
        logger.error(
            f"Failed to connect to MQTT broker. Return code: {rc}. The client will attempt to reconnect automatically."
        )


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning(
            f"Disconnected from MQTT broker unexpectedly (code: {rc}). Client will try to reconnect in 2 minutes."
        )
    else:
        logger.info("Disconnected from MQTT broker gracefully.")


def on_message(client, userdata, msg):
    logger.debug(f"Received message on topic {msg.topic}")
    if msg.topic == MQTT_TOPIC_SENSOR:
        handle_temperature_humidity(msg.payload.decode())
    elif msg.topic == MQTT_TOPIC_LEVEL:
        handle_level(msg.payload.decode())


def start_mqtt_listener():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.enable_logger(logger)
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.reconnect_delay_set(min_delay=120, max_delay=120)

    client.loop_start()

    logger.info(f"Initiating MQTT connection to {MQTT_BROKER}:{MQTT_PORT}")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        logger.error(f"MQTT connection attempt failed: {e}. Retrying in 2 minutes...")
