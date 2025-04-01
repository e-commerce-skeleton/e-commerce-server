from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from io import BytesIO
import pandas as pd
from src.app.database.session import get_db

from src.app.services.stock.excel_import import add_products_from_excel, delete_products_from_excel
from src.app.crud.product import create_product, update_product, delete_product
from src.app.crud.category import create_category, get_category_by_name

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/import/")
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Invalid file format. Only Excel files are allowed.")
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    add_products_from_excel(df, db)
    return {"message": "Products imported successfully"}


@router.post("/delete/")
async def delete_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Invalid file format. Only Excel files are allowed.")
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    delete_products_from_excel(df, db)
    return {"message": "Products deleted successfully"}


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
    stock: int = 0,
    categories: str = "",
    db: Session = Depends(get_db),
):
    product = create_product(
        db, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories
    )
    return {"message": "Product added successfully", "product_id": product.prod_id}


@router.put("/products/{prodId}")
def edit_product(
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
    updated_product = update_product(
        db, prodId, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories
    )
    return {"message": "Product updated successfully", "product_id": updated_product.prod_id}


@router.delete("/products/{prodId}")
def remove_product(prodId: int, db: Session = Depends(get_db)):
    delete_product(db, prodId)
    return {"message": "Product deleted successfully", "product_id": prodId}