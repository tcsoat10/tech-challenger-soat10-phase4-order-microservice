from typing import List
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from src.core.domain.entities.order_status import OrderStatus
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.shared.identity_map import IdentityMap
from src.adapters.driven.repositories.models.order_status_model import OrderStatusModel


class OrderStatusRepository(IOrderStatusRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map = IdentityMap.get_instance()

    def create(self, order_status: OrderStatus) -> OrderStatus:
        if order_status.id is not None:
            existing = self.identity_map.get(OrderStatus, order_status.id)
            if existing:
                self.identity_map.remove(existing)
        
        order_status_model = OrderStatusModel.from_entity(order_status)
        self.db_session.add(order_status_model)
        self.db_session.commit()
        self.db_session.refresh(order_status_model)
        return order_status_model.to_entity()

    def exists_by_status(self, status: str) -> bool:
        return self.db_session.query(exists().where(OrderStatusModel.status == status)).scalar()

    def get_by_status(self, status: str) -> OrderStatus:
        order_status_model =  self.db_session.query(OrderStatusModel).filter(OrderStatusModel.status == status).first()
        if order_status_model is None:
            return None
        return order_status_model.to_entity()

    def get_by_id(self, order_status_id: int) -> OrderStatus:
        order_status_model =  self.db_session.query(OrderStatusModel).filter(
            OrderStatusModel.id == order_status_id
        ).first()
        if order_status_model is None:
            return None
        return order_status_model.to_entity()

    def get_all(self, include_deleted: bool = False) -> List[OrderStatus]:
        query = self.db_session.query(OrderStatusModel)
        if not include_deleted:
            query = query.filter(OrderStatusModel.inactivated_at.is_(None))
        order_status_models = query.all()
        return [order_status.to_entity() for order_status in order_status_models]

    def update(self, order_status: OrderStatus) -> OrderStatus:
        if order_status.id is not None:
            existing = self.identity_map.get(OrderStatus, order_status.id)
            if existing:
                self.identity_map.remove(existing)

        order_status_model = OrderStatusModel.from_entity(order_status)
        self.db_session.merge(order_status_model)
        self.db_session.commit()
        return order_status_model.to_entity()

    def delete(self, order_status: OrderStatus) -> None:
        order_status_model =  self.db_session.query(OrderStatusModel).filter(
            OrderStatusModel.id == order_status.id
        ).first()
        if order_status_model:
            self.db_session.delete(order_status_model)
            self.db_session.commit()
            self.identity_map.remove(order_status_model.to_entity())
