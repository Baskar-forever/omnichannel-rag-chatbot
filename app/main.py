from fastapi import FastAPI

from app.api.health import (
    router as health_router
)

from app.api.chat import (
    router as chat_router
)

from fastapi.middleware.cors import CORSMiddleware

from app.api.whatsapp import (
    router as whatsapp_router
)


app = FastAPI(
    title="ZenFuture Chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    health_router
)

app.include_router(
    chat_router
)

app.include_router(
    whatsapp_router,
    prefix="/api"
)