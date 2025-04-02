from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.app.models.product import ProductModel
from src.app.services.stock.category_sync import sync_categories_from_row, remove_unused_categories

def get_product_by_id(db: Session, prod_id: int):
    return db.query(ProductModel).filter(ProductModel.prod_id == prod_id).first()

def create_product(db: Session, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories):

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

    product.categories = sync_categories_from_row({"categories": categories}, db)
    db.commit()

    return product

def update_product(db: Session, prod_id, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories):
    product = get_product_by_id(db, prod_id)

    for field, value in {
        "name": name, "img_url": img_url, "alt_text": alt_text, "description": description,
        "current_price": current_price, "prev_price": prev_price, "payment_method": payment_method,
        "detail": detail, "stock": stock
    }.items():
        if value is not None:
            setattr(product, field, value)

    if categories is not None:
        product.categories.clear()
        product.categories = sync_categories_from_row({"categories": categories}, db)

    db.commit()
    remove_unused_categories(db)
    return product

def delete_product(db: Session, prod_id: int):
    product = get_product_by_id(db, prod_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.categories.clear()
    db.delete(product)
    db.commit()

    remove_unused_categories(db)
