from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.mqtt.mqtt_listener import start_mqtt_listener

app = FastAPI(
    title="Peat Data API",
    description="Database operations API, integrating mobile app, embedded system, and notification service.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def startup_event():
    start_mqtt_listener()
