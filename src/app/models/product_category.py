# src/app/models/product_category.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from src.app.database.session import Base

product_category_table = Table(
    "product_category",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.prod_id"), primary_key=True),
    Column("category_name", String(255), ForeignKey("categories.name"), primary_key=True)
)
