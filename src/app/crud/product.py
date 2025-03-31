from sqlalchemy.orm import Session
from src.app.models.product import ProductModel

def get_product_by_id(db: Session, prod_id: int):
    return db.query(ProductModel).filter(ProductModel.prod_id == prod_id).first()

def create_product(db: Session, prod_id: int, name: str, img_url: str, alt_text: str, description: str, current_price: float, prev_price: float, payment_method: str, detail: str):
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
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product: ProductModel, name: str, img_url: str, alt_text: str, description: str, current_price: float, prev_price: float, payment_method: str, detail: str):
    product.name = name
    product.img_url = img_url
    product.alt_text = alt_text
    product.description = description
    product.current_price = current_price
    product.prev_price = prev_price
    product.payment_method = payment_method
    product.detail = detail
    db.commit()
    db.refresh(product)
    return product
