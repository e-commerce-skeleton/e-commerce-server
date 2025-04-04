from fastapi import HTTPException, UploadFile
import pandas as pd
from sqlalchemy.orm import Session
from src.app.models.product import ProductModel
from src.app.models.category import CategoryModel

def validate_excel(file: UploadFile):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Invalid file format. Only Excel files are allowed.")
    

def validate_excel_format(df: pd.DataFrame, required_columns: list):
    """Verifica que el archivo Excel tenga las columnas necesarias."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing_columns)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")

def validate_product_fields(row):
    required_fields = ["name", "img_url", "alt_text", "description", "current_price", "payment_method"]
    
    for field in required_fields:
        if field not in row or pd.isna(row[field]):
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    if not isinstance(row["current_price"], (int, float)) or row["current_price"] < 0:
        raise HTTPException(status_code=400, detail="Invalid value for current_price. Must be a positive number.")
    
    if "stock" in row and (not isinstance(row["stock"], int) or row["stock"] < 0):
        raise HTTPException(status_code=400, detail="Invalid value for stock. Must be a non-negative integer.")

    return True

def check_unique_product_name(db: Session, name: str):
    if db.query(ProductModel).filter(ProductModel.name == name).first():
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    
def check_product_exists(db: Session, prod_id: str):
    if not db.query(ProductModel).filter(ProductModel.prod_id == prod_id).first():
        raise HTTPException(status_code=404, detail="Product not found")

def check_category_exists(db: Session, name: str):
    if not db.query(CategoryModel).filter(CategoryModel.name == name).first():
        raise HTTPException(status_code=404, detail="Category not found")
