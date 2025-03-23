# src/app/models/user.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.app.database.session import Base

class UserModel(Base):
    __tablename__ = 'users'

    user_id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(255), index=True)

    # Relación con otros modelos si es necesario
