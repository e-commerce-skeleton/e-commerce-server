from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from src.app.database.session import get_db
from src.app.utils.sync_product_relations import sync_associations

router = APIRouter()

@router.post("/import-products/")
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Leer el archivo Excel en memoria
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Sincronizamos los productos y las categorías
    sync_associations(df, db)

    return {"message": "sync OK"}
