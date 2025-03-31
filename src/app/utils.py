from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from src.app.models.product import ProductModel
from src.app.models.category import CategoryModel

def sync_products_and_categories(df: pd.DataFrame, db: Session):
    product_ids_from_excel = set()

    for _, row in df.iterrows():
        # Sincronizar producto
        product = sync_product_from_row(row, db)

        # Sincronizar categorías
        categories = sync_categories_from_row(row, db)
        
        # Asegura que las categorías estén en la base de datos
        db.flush()  
        
        # Asociar producto con las categorías
        product.categories = categories
        product_ids_from_excel.add(row.get("prodId"))

    # Eliminar productos que no están en el archivo
    remove_deleted_products(db, product_ids_from_excel)

    # Eliminar categorías no asociadas a productos
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

    # Buscar el producto en la base de datos
    product = db.query(ProductModel).filter(ProductModel.prod_id == prod_id).first()

    # Si el producto no existe, lo creamos
    if not product:
        product = ProductModel(
            prod_id=prod_id,
            name=name,
            img_url=img_url,
            alt_text=alt_text,
            description=description,
            current_price=current_price,
            prev_price=prev_price,
            payment_method=payment_method,
            detail=detail
        )
        db.add(product)
    else:
        # Si el producto ya existe, actualizamos los campos que hayan cambiado
        product.name = name
        product.img_url = img_url
        product.alt_text = alt_text
        product.description = description
        product.current_price = current_price
        product.prev_price = prev_price
        product.payment_method = payment_method
        product.detail = detail

    return product

def sync_categories_from_row(row, db: Session):
    category_names = [cat.strip() for cat in row.get("categories").split(",")]
    categories = []
    
    for cat_name in category_names:

        category = db.query(CategoryModel).filter(CategoryModel.name == cat_name).first()
        
        if not category:
            category = CategoryModel(name=cat_name)
            db.add(category)
        
        categories.append(category)
    
    return categories


def remove_deleted_products(db: Session, product_ids_from_excel: set):
    # Eliminar productos que no están en el archivo
    products_in_db = db.query(ProductModel).filter(ProductModel.prod_id.notin_(product_ids_from_excel)).all()
    for product in products_in_db:
        # Eliminar asociaciones producto-categoría
        product.categories.clear()
        db.delete(product)


def remove_unused_categories(db: Session):
    # Eliminar categorías no asociadas a productos
    categories_in_db = db.query(CategoryModel).all()
    for category in categories_in_db:
        if not category.products:
            db.delete(category)
