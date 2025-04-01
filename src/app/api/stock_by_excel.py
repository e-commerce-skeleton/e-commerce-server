from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from src.app.database.session import get_db
from src.app.services.sync_products_from_excel import add_products_from_excel, delete_products_from_excel

router = APIRouter()

@router.post("/import-products/")
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file format. Only Excel files are allowed.")
    
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    required_columns = {"name", "imgUrl", "altText", "description", "currentPrice", "categories"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"Missing required columns: {required_columns - set(df.columns)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")

    add_products_from_excel(df, db)

    return {"message": "Products synchronized successfully"}

@router.post("/delete-products/")
async def delete_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file format. Only Excel files are allowed.")
    
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    if df.empty or "prodId" not in df.columns:
        raise HTTPException(status_code=400, detail="Invalid file format. It must contain a 'prodId' column.")

    delete_products_from_excel(df, db)

    return {"message": "Products deleted successfully"}
