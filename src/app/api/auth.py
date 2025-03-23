# src/app/api/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from src.app.database.session import get_db
from src.app.crud.user import get_user_by_email, create_user
from src.app.schemas.token import TokenData
from src.app.config import google_client_id

router = APIRouter()

@router.post("/auth/google")
async def google_auth(token_data: TokenData, db: Session = Depends(get_db)):
    try:
        # Verificar el token con Google
        id_info = id_token.verify_oauth2_token(token_data.token, requests.Request(), google_client_id)
        
        user_id = id_info["sub"]  # Google user ID
        email = id_info["email"]
        name = id_info.get("name", "")
        
        # Verificar si el usuario existe
        user = get_user_by_email(db, email)
        if not user:
            # Crear el nuevo usuario
            user = create_user(db, user_id, email, name)
        
        return {"message": "User logged in", "user_id": user.user_id, "email": user.email, "name": user.name}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
