from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from fastapi import HTTPException
from src.app.models.product import ProductModel
from src.app.models.category import CategoryModel
from src.app.crud.product import create_product, get_product_by_id, update_product
from src.app.crud.category import create_category, get_category_by_name

def validate_excel_format(df: pd.DataFrame, required_columns: list):
    """Verifica que el archivo Excel tenga las columnas necesarias."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing_columns)}")

def add_products_from_excel(df: pd.DataFrame, db: Session):
    required_columns = ["name", "imgUrl", "altText", "description", "currentPrice", "categories"]
    validate_excel_format(df, required_columns)
    
    for _, row in df.iterrows():
        product = sync_product_from_row(row, db)
        categories = sync_categories_from_row(row, db)
        product.categories = categories
        db.commit()

def delete_products_from_excel(df: pd.DataFrame, db: Session):
    required_columns = ["prodId"]
    validate_excel_format(df, required_columns)
    
    product_ids_to_delete = set(df["prodId"].dropna().astype(int))
    products_to_delete = db.query(ProductModel).filter(ProductModel.prod_id.in_(product_ids_to_delete)).all()
    
    for product in products_to_delete:
        product.categories.clear()
        db.delete(product)
    db.commit()
    remove_unused_categories(db)

def sync_product_from_row(row, db: Session):
    name = row.get("name")
    img_url = row.get("imgUrl")
    alt_text = row.get("altText")
    description = row.get("description")
    current_price = row.get("currentPrice")
    prev_price = row.get("prevPrice") if not pd.isna(row.get("prevPrice")) else None
    payment_method = row.get("paymentMethod")
    detail = row.get("detail") if not pd.isna(row.get("detail")) else None
    stock = row.get("stock", 0)
    
    if pd.isna(name) or pd.isna(current_price):
        raise HTTPException(status_code=400, detail="Missing required product fields: 'name' and 'currentPrice'")

    product = ProductModel(
        name=name,
        img_url=img_url,
        alt_text=alt_text,
        description=description,
        current_price=current_price,
        prev_price=prev_price,
        payment_method=payment_method,
        detail=detail,
        stock=stock,
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product

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
