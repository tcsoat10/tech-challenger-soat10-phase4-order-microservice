from typing import List
from src.adapters.driven.repositories.models.category_model import CategoryModel
from src.adapters.driven.repositories.models.order_model import OrderModel
from src.adapters.driven.repositories.models.product_model import ProductModel
from src.adapters.driven.repositories.models.order_item_model import OrderItemModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.order_item import OrderItem
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from sqlalchemy.orm import Session


class OrderItemRepository(IOrderItemRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create(self, order_item: OrderItem) -> OrderItem:
        if order_item.id is not None:
            existing_order_item = self.identity_map.get(OrderItem, order_item.id)
            if existing_order_item:
                self.identity_map.remove(existing_order_item)

        order_item_model = OrderItemModel.from_entity(order_item)
        self.db_session.add(order_item_model)
        self.db_session.commit()
        self.db_session.refresh(order_item_model)
        return order_item_model.to_entity()

    def get_by_order_id(self, order_id: int, include_deleted: bool = False) -> List[OrderItem]:
        query = self.db_session.query(OrderItemModel).filter(OrderItemModel.order_id == order_id)
        if not include_deleted:
            query = query.filter(OrderItemModel.inactivated_at.is_(None))
        order_item_models = query.all()
        return [order_item_model.to_entity() for order_item_model in order_item_models]

    def get_by_product_name(self, order_id: int, product_name: str) -> OrderItem:
        order_item_model = (
            self.db_session.query(OrderItemModel)
                .filter(OrderItemModel.order_id == order_id)
                .join(OrderItemModel.product)
                .filter(ProductModel.name == product_name)
                .first()
        )
        if order_item_model is None:
            return None
        return order_item_model.to_entity()

    def get_by_id(self, order_item_id: int) -> OrderItem:
        order_item_model = self.db_session.query(OrderItemModel).filter(OrderItemModel.id == order_item_id).first()
        if order_item_model is None:
            return None
        return order_item_model.to_entity()

    def get_all(self, include_deleted: bool = False) -> List[OrderItem]:
        query = self.db_session.query(OrderItemModel)
        if not include_deleted:
            query = query.filter(OrderItemModel.inactivated_at.is_(None))
        order_item_models = query.all()
        return [order_item_model.to_entity() for order_item_model in order_item_models]
    
    def update(self, order_item: OrderItem) -> OrderItem:
        if order_item.id is not None:
            existing_order_item = self.identity_map.get(OrderItem, order_item.id)
            if existing_order_item:
                self.identity_map.remove(existing_order_item)

        order_item_model = OrderItemModel.from_entity(order_item)
        order_item_model.product = ProductModel.from_entity(order_item.product)
        order_item_model.order = OrderModel.from_entity(order_item.order)
        
        self.db_session.merge(order_item_model)
        self.db_session.commit()

        order_item_model = OrderItemModel.from_entity(self.get_by_id(order_item.id))
        return order_item_model.to_entity()
    
    
    def delete(self, order_item: OrderItem) -> None:
        order_item_model = (
            self.db_session.query(OrderItemModel)
                .filter(OrderItemModel.id == order_item.id)
                .first()
        )
        if order_item_model:
            self.db_session.delete(order_item_model)
            self.db_session.commit()
            self.identity_map.remove(order_item)
