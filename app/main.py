from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.mqtt.mqtt_listener import start_mqtt_listener
from app.core.constants import TAGS


app = FastAPI(
    title="Peat Data API",
    description="API for managing Peat Data operations, integrating **IoT devices** (via MQTT), **mobile applications** (historical data), and **notification services**, along with **administrative functions**.",
    version="2.0.0",
    openapi_tags=TAGS,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(router)


@app.on_event("startup")
def startup_event():
    start_mqtt_listener()
