from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permitir solicitudes desde el frontend 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

GOOGLE_CLIENT_ID = "52806677381-9gutdb1kc1j7c1l9o0c1qc300e6af72l.apps.googleusercontent.com"

class TokenData(BaseModel):
    token: str

# Simulated database (Replace with actual DB logic)
fake_db = {}

@app.post("/auth/google")
async def google_auth(data: TokenData):
    try:
        # Verifica el token con Google
        id_info = id_token.verify_oauth2_token(
            data.token, requests.Request(), GOOGLE_CLIENT_ID
        )

        user_id = id_info["sub"]  # Google user ID
        email = id_info["email"]
        name = id_info.get("name", "")

        # Lógica para simular la base de datos
        if email not in fake_db:
            fake_db[email] = {"user_id": user_id, "email": email, "name": name}
            return {"message": "User registered", "user_id": user_id, "email": email, "name": name}
        else:
            return {"message": "User logged in", "user_id": user_id, "email": email, "name": name}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

