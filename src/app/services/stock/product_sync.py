from sqlalchemy.orm import Session
import pandas as pd
from fastapi import HTTPException
from src.app.models.product import ProductModel
from src.app.crud.product import create_product


def sync_product_from_row(row, db: Session):
    name = row.get("name")
    img_url = row.get("imgUrl")
    alt_text = row.get("altText")
    description = row.get("description")
    current_price = row.get("currentPrice")
    prev_price = row.get("prevPrice") if not pd.isna(row.get("prevPrice")) else None
    payment_method = row.get("paymentMethod") if not pd.isna(row.get("paymentMethod")) else None
    detail = row.get("detail") if not pd.isna(row.get("detail")) else None
    stock = row.get("stock", 0)
    categories = row.get("categories") if not pd.isna(row.get("categories")) else None

    if pd.isna(name) or pd.isna(current_price) or pd.isna(payment_method) or pd.isna(categories):
        raise HTTPException(status_code=400, detail="Missing required product fields")

    product = create_product(db, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories)
    
    return product

