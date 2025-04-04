from src.app.models.product import ProductModel
from src.app.models.category import CategoryModel
from src.app.schemas.product import ProductSchema
from src.app.schemas.category import CategorySchema

def product_model_to_schema(product_model: ProductModel) -> ProductSchema:
    return ProductSchema(
        prod_id=product_model.prod_id,
        img_url=product_model.img_url,
        alt_text=product_model.alt_text,
        description=product_model.description,
        name=product_model.name,
        current_price=product_model.current_price,
        prev_price=product_model.prev_price,
        payment_method=product_model.payment_method,
        detail=product_model.detail,
        stock=product_model.stock,
        categories=[category.name for category in product_model.categories]
    )

def category_model_to_schema(category_model: CategoryModel) -> CategorySchema:
    return CategorySchema(
        name=category_model.name,
        products=[product_model_to_schema(product_model) for product_model in category_model.products]
    )
