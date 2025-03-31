# src/app/models/category.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.app.database.session import Base
from src.app.models.product_category import product_category_table

class CategoryModel(Base):
    __tablename__ = "categories"

    name = Column(String(255), primary_key=True, index=True)

    products = relationship("ProductModel", secondary=product_category_table, back_populates="categories")
