from sqlalchemy.orm import Session
from src.app.models.category import CategoryModel
from src.app.crud.category import get_category_by_name, create_category

def sync_categories_from_row(row, db: Session):
    category_names = [cat.strip() for cat in str(row.get("categories", "")).split(",") if cat.strip()]
    categories = []
    for cat_name in category_names:
        category = get_category_by_name(db, cat_name) or create_category(db, cat_name)
        categories.append(category)
    return categories

def remove_unused_categories(db: Session):
    categories_in_db = db.query(CategoryModel).all()
    for category in categories_in_db:
        if not category.products:
            db.delete(category)
    db.commit()