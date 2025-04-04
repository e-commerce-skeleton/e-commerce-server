# src/app/schemas/category.py
from pydantic import BaseModel
from typing import List
from .product import ProductSchema

class CategorySchema(BaseModel):
    name: str
    products: List[ProductSchema] = []

    class Config:
        orm_mode = True