# src/app/schemas/product.py
from pydantic import BaseModel
from typing import Optional, List
from src.app.schemas.category import CategorySchema

class ProductSchema(BaseModel):
    prod_id: int
    img_url: str
    alt_text: str
    description: str
    name: str
    current_price: float
    stock: int
    prev_price: Optional[float] = None
    payment_method: Optional[str] = None
    detail: Optional[str] = None
    categories: List[CategorySchema] = []

    class Config:
        orm_mode = True