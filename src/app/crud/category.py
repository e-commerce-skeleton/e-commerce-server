from sqlalchemy.orm import Session
from src.app.models.category import CategoryModel

def get_category_by_name(db: Session, name: str):
    return db.query(CategoryModel).filter(CategoryModel.name == name).first()

def create_category(db: Session, name: str):
    category = CategoryModel(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
