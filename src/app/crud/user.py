# src/app/crud/user.py
from sqlalchemy.orm import Session
from src.app.models.user import UserModel

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def create_user(db: Session, user_id: str, email: str, name: str):
    db_user = UserModel(user_id=user_id, email=email, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
