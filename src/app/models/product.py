# src/app/models/product.py
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from src.app.database.session import Base
from src.app.models.product_category import product_category_table

class ProductModel(Base):
    __tablename__ = "products"

    prod_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    img_url = Column(String(255), nullable=False)
    alt_text = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    current_price = Column(Float, nullable=False)
    prev_price = Column(Float, nullable=True)
    payment_method = Column(String(255), nullable=True)
    detail = Column(String(255), nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    
    categories = relationship("CategoryModel", secondary=product_category_table, back_populates="products")

