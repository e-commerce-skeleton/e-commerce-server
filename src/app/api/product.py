from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from src.app.models.product import ProductModel
from src.app.models.category import CategoryModel
from src.app.database.session import get_db
from src.app.utils import sync_products_and_categories  # Importamos la función que manejará la lógica

router = APIRouter()

@router.post("/import-products/")
async def import_products(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Leer el archivo Excel en memoria
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Sincronizamos los productos y las categorías
    sync_products_and_categories(df, db)

    return {"message": "Productos y categorías sincronizados correctamente"}
