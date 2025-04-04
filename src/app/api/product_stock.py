from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from src.app.database.session import get_db
from io import BytesIO
import pandas as pd
from src.app.services.stock.excel_import import add_products_from_excel, delete_products_from_excel
from src.app.services.stock.validation import validate_excel
from src.app.crud.product import create_product, update_product, delete_product, get_product_by_id, get_products
from src.app.crud.category import get_category_by_name, get_categories
from src.app.services.stock.validation import check_unique_product_name, check_product_exists, check_category_exists
from typing import List
from src.app.schemas.product import ProductSchema
from src.app.schemas.category import CategorySchema
from src.app.services.converters import product_model_to_schema, category_model_to_schema

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
    create_product(
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
    update_product(
        db, prod_id, name, img_url, alt_text, description, current_price, prev_price, payment_method, detail, stock, categories
    )
    return {"message": "Product updated successfully"}


@router.delete("/products/{prod_id}")
def delete_product(prod_id: int, db: Session = Depends(get_db)):
    delete_product(db, prod_id)
    return {"message": "Product deleted successfully"}

@router.get("/products/", response_model=List[ProductSchema])
def get_products_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products_models = get_products(db, skip=skip, limit=limit)
    products_schemas = [product_model_to_schema(product_model) for product_model in products_models]
    return products_schemas

@router.get("/products/{prod_id}", response_model=ProductSchema)
def get_product(prod_id: int, db: Session = Depends(get_db)):
    check_product_exists(db, prod_id)
    product_model = get_product_by_id(db, prod_id)
    return product_model_to_schema(product_model)

@router.get("/categories/", response_model=List[str])
def get_categories_names(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories_model = get_categories(db, skip=skip, limit=limit)
    return [category_model.name for category_model in categories_model]

@router.get("/categories/{name}", response_model=CategorySchema)
def get_category_products(name: str, db: Session = Depends(get_db)):
    check_category_exists(db, name)
    category_model = get_category_by_name(db, name)
    return category_model_to_schema(category_model)