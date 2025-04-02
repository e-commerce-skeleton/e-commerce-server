# src/app/main.py
from fastapi import FastAPI
from src.app.api import auth
from src.app.api import product_stock
from fastapi.middleware.cors import CORSMiddleware
from .config import db_host, client_port

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{db_host}:{client_port}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(product_stock.router)
