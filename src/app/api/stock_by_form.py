from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.app.database.session import get_db
from src.app.models.product import ProductModel
from src.app.models.category import CategoryModel
from src.app.crud.product import create_product, get_product_by_id, update_product
from src.app.crud.category import create_category, get_category_by_name

router = APIRouter()

@router.post("/products/")
def add_product(
    name: str,
    img_url: str,
    alt_text: str,
    description: str,
    current_price: float,
    prev_price: float = None,
    payment_method: str = None,
    detail: str = None,
    stock: int = 0,  # Por defecto 0
    categories: str = "",
    db: Session = Depends(get_db),
):
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
    db.refresh(product)  # Para obtener el ID autogenerado

    category_names = [cat.strip() for cat in categories.split(",") if cat.strip()]
    for cat_name in category_names:
        category = get_category_by_name(db, cat_name) or create_category(db, cat_name)
        product.categories.append(category)

    db.commit()

    return {"message": "Product added successfully", "product_id": product.prod_id}


@router.put("/products/{prodId}")
def update_product(
    prodId: int,
    name: str = None,
    img_url: str = None,
    alt_text: str = None,
    description: str = None,
    current_price: float = None,
    prev_price: float = None,
    payment_method: str = None,
    detail: str = None,
    stock: int = None,
    categories: str = None,
    db: Session = Depends(get_db),
):
    product = get_product_by_id(db, prodId)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Solo actualiza los campos enviados en la query
    if name is not None:
        product.name = name
    if img_url is not None:
        product.img_url = img_url
    if alt_text is not None:
        product.alt_text = alt_text
    if description is not None:
        product.description = description
    if current_price is not None:
        product.current_price = current_price
    if prev_price is not None:
        product.prev_price = prev_price
    if payment_method is not None:
        product.payment_method = payment_method
    if detail is not None:
        product.detail = detail
    if stock is not None:
        product.stock = stock

    if categories is not None:
        category_names = [cat.strip() for cat in categories.split(",") if cat.strip()]
        product.categories.clear()  # Se eliminan las categorías previas
        for cat_name in category_names:
            category = get_category_by_name(db, cat_name) or create_category(db, cat_name)
            product.categories.append(category)

    db.commit()

    return {"message": "Product updated successfully", "product_id": prodId}


@router.delete("/products/{prodId}")
def delete_product(prodId: str, db: Session = Depends(get_db)):
    product = get_product_by_id(db, prodId)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Eliminar la relación con las categorías
    product.categories.clear()
    # Remueve categorias huerfanas (sin productos)
    categories_in_db = db.query(CategoryModel).all()
    for category in categories_in_db:
        if not category.products:
            db.delete(category)

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully", "product_id": prodId}



