from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from io import BytesIO
import pandas as pd
from src.app.database.session import get_db
from src.app.services.stock.excel_import import add_products_from_excel, delete_products_from_excel
from src.app.services.stock.validation import validate_excel

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/import/")
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    validate_excel(file)
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    created_count = add_products_from_excel(df, db)
    return {"message": f"Imported {created_count} products successfully"}


@router.post("/delete/")
async def delete_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    validate_excel(file)
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    deleted_count = delete_products_from_excel(df, db)
    return {"message": f"Deleted {deleted_count} products successfully"}
