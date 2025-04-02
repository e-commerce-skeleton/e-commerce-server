from sqlalchemy.orm import Session
import pandas as pd
from fastapi import HTTPException
from src.app.models.product import ProductModel
from src.app.crud.product import create_product, get_product_by_id
from .validation import validate_product_fields

def sync_product_from_row(row, db: Session):
    name = row.get("name")
    img_url = row.get("img_url")
    alt_text = row.get("alt_text")
    description = row.get("description")
    current_price = row.get("current_price")
    prev_price = row.get("prev_price") if not pd.isna(row.get("prev_price")) else None
    payment_method = row.get("payment_method") if not pd.isna(row.get("payment_method")) else None
    detail = row.get("detail") if not pd.isna(row.get("detail")) else None
    stock = row.get("stock", 0)
    categories = row.get("categories") if not pd.isna(row.get("categories")) else None

    validate_product_fields(row)

    if db.query(ProductModel).filter(ProductModel.name == name).first():
        return None
    
    product = create_product(db, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories)
    return product

