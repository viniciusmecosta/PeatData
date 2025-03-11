from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Peat Data API",
    description="This API intermediates the interaction between Firebase, the app, and the embedded system.",  # Descrição da API
    version="1.0.0",
)

app.include_router(router)
