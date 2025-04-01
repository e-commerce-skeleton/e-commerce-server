from sqlalchemy.orm import Session
import pandas as pd
from src.app.models.product import ProductModel
from src.app.services.stock.product_sync import sync_product_from_row
from src.app.services.stock.category_sync import sync_categories_from_row, remove_unused_categories
from src.app.services.stock.validation import validate_excel_format

def add_products_from_excel(df: pd.DataFrame, db: Session):
    required_columns = ["name", "imgUrl", "altText", "description", "currentPrice", "categories"]
    validate_excel_format(df, required_columns)

    for _, row in df.iterrows():
        sync_product_from_row(row, db)
        

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
