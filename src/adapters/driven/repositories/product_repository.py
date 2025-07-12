from typing import List, Optional
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from src.adapters.driven.repositories.models.category_model import CategoryModel
from src.adapters.driven.repositories.models.product_model import ProductModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.product import Product
from src.core.ports.product.i_product_repository import IProductRepository

class ProductRepository(IProductRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, product: Product) -> Product:
        existing = self.identity_map.get(Product, product.id)
        if existing:
            self.identity_map.remove(existing)

        product_model = ProductModel.from_entity(product)
        product_model.category = self.db_session.query(CategoryModel).filter(CategoryModel.id == product.category.id).first()

        self.db_session.add(product_model)
        self.db_session.commit()
        self.db_session.refresh(product_model)
        return product_model.to_entity()

    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(ProductModel.name == name)).scalar()

    def get_by_name(self, name: str) -> Product:
        product_model = self.db_session.query(ProductModel).filter(ProductModel.name == name).first()
        if not product_model:
            return None
        return product_model.to_entity()

    def get_by_id(self, product_id: int) -> Product:
        product_model = self.db_session.query(ProductModel).filter(ProductModel.id == product_id).first()
        if not product_model:
            return None
        return product_model.to_entity()

    def get_all(self, categories: Optional[List[str]] = None, include_deleted: Optional[bool] = False) -> List[Product]:
        query = self.db_session.query(ProductModel)

        if not include_deleted:
            query = query.filter(ProductModel.inactivated_at.is_(None))

        if categories:
            query = query.filter(ProductModel.category.has(CategoryModel.name.in_(categories)))

        product_models = query.all()
        return [product_model.to_entity() for product_model in product_models]

    def update(self, product: Product) -> Product:
        existing = self.identity_map.get(Product, product.id)
        if existing:
            self.identity_map.remove(existing)
        
        product_model = ProductModel.from_entity(product)
        product_model.category = CategoryModel.from_entity(product.category)

        self.db_session.merge(product_model)
        self.db_session.commit()

        return product_model.to_entity()

    def delete(self, product: Product) -> None:
        product_model = self.db_session.query(ProductModel).filter(ProductModel.id == product.id).first()
        if product_model:
            self.db_session.delete(product)
            self.db_session.commit()
            self.identity_map.remove(product_model.to_entity())
