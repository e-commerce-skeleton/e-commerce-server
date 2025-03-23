# src/app/main.py
from fastapi import FastAPI
from src.app.api import auth
from fastapi.middleware.cors import CORSMiddleware
from .config import db_host, client_port

app = FastAPI()

# Permitir solicitudes desde el frontend 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{db_host}:{client_port}"],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.include_router(auth.router)
