from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from src.app.database.session import get_db
from io import BytesIO
import pandas as pd
from src.app.services.stock.excel_import import add_products_from_excel, delete_products_from_excel
from src.app.services.stock.validation import validate_excel
from src.app.crud.product import create_product, update_product, delete_product
from src.app.services.stock.validation import check_unique_product_name, check_product_exists

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/import/")
async def import_many_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    validate_excel(file)
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    created_count = add_products_from_excel(df, db)
    return {"message": f"Imported {created_count} products successfully"}


@router.delete("/delete/")
async def delete_many_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    validate_excel(file)
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    deleted_count = delete_products_from_excel(df, db)
    return {"message": f"Deleted {deleted_count} products successfully"}


@router.post("/products/")
def import_product(
    name: str,
    img_url: str,
    alt_text: str,
    description: str,
    current_price: float,
    prev_price: float = None,
    payment_method: str = None,
    detail: str = None,
    stock: int = 0,
    categories: str = "",
    db: Session = Depends(get_db),
):
    check_unique_product_name(db, name)
    product = create_product(
        db, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories
    )
    return {"message": "Product added successfully"}


@router.put("/products/{prod_id}")
def update_product(
    prod_id: int,
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
    check_product_exists(db, prod_id)
    updated_product = update_product(
        db, prod_id, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories
    )
    return {"message": "Product updated successfully"}


@router.delete("/products/{prod_id}")
def delete_product(prod_id: int, db: Session = Depends(get_db)):
    delete_product(db, prod_id)
    return {"message": "Product deleted successfully"}