from fastapi import HTTPException
import pandas as pd

def validate_excel_format(df: pd.DataFrame, required_columns: list):
    """Verifica que el archivo Excel tenga las columnas necesarias."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing_columns)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")
