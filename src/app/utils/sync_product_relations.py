from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from src.app.models.product import ProductModel
from src.app.models.category import CategoryModel
from src.app.crud.product import create_product, get_product_by_id, update_product
from src.app.crud.category import create_category, get_category_by_name

def sync_associations(df: pd.DataFrame, db: Session):
    product_ids_from_excel = set()

    for _, row in df.iterrows():
        product = sync_product_from_row(row, db)

        categories = sync_categories_from_row(row, db)
        
        product.categories = categories
        product_ids_from_excel.add(row.get("prodId"))

    remove_deleted_products(db, product_ids_from_excel)

    remove_unused_categories(db)

    db.commit()


def sync_product_from_row(row, db: Session):
    prod_id = row.get("prodId")
    name = row.get("name")
    img_url = row.get("imgUrl")
    alt_text = row.get("altText")
    description = row.get("description")
    current_price = row.get("currentPrice")
    prev_price = row.get("prevPrice", None)
    payment_method = row.get("paymentMethod")
    detail = row.get("detail", None)
    
    # Verificar si los campos opcionales son NaN y reemplazar por None
    if isinstance(prev_price, float) and np.isnan(prev_price):
        prev_price = None
    if isinstance(detail, float) and np.isnan(detail):
        detail = None

    product = get_product_by_id(db, prod_id)

    if not product:
        product = create_product(db, prod_id, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail)
    else:
        update_product(db, product, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail)

    return product

def sync_categories_from_row(row, db: Session):
    category_names = [cat.strip() for cat in row.get("categories").split(",")]
    categories = []
    
    for cat_name in category_names:

        category = get_category_by_name(db, cat_name)
        
        if not category:
            category = create_category(db, cat_name)
        
        categories.append(category)
    
    return categories


def remove_deleted_products(db: Session, product_ids_from_excel: set):
    products_in_db = db.query(ProductModel).filter(ProductModel.prod_id.notin_(product_ids_from_excel)).all()
    for product in products_in_db:
        product.categories.clear()
        db.delete(product)


def remove_unused_categories(db: Session):
    categories_in_db = db.query(CategoryModel).all()
    for category in categories_in_db:
        if not category.products:
            db.delete(category)
