from typing import List, Optional
from src.constants.order_status import OrderStatusEnum
from src.adapters.driven.repositories.models.order_status_movement_model import OrderStatusMovementModel
from src.adapters.driven.repositories.models.order_model import OrderModel
from src.adapters.driven.repositories.models.order_status_model import OrderStatusModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.order import Order
from src.core.ports.order.i_order_repository import IOrderRepository
from sqlalchemy.orm import Session
from sqlalchemy import case

class OrderRepository(IOrderRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create(self, order: Order) -> Order:
        if order.id is not None:
            existing_order = self.get_by_id(order.id)
            if existing_order:
                self.identity_map.remove(existing_order)

        order_model = OrderModel.from_entity(order)
        self.db_session.add(order_model)
        self.db_session.commit()
        self.db_session.refresh(order_model)
        return order_model.to_entity()

    def get_by_customer_id(self, id_customer: int) -> List[Order]:
        order_models = self.db_session.query(OrderModel).filter(OrderModel.id_customer == id_customer, OrderModel.inactivated_at.is_(None)).all()
        return [order.to_entity() for order in order_models]
    
    def get_by_employee_id(self, id_employee: int) -> List[Order]:
        order_models = self.db_session.query(OrderModel).filter(OrderModel.id_employee == id_employee, OrderModel.inactivated_at.is_(None)).all()
        return [order.to_entity() for order in order_models]
    
    def get_by_payment_id(self, id_payment: int) -> Order:
        order_model = self.db_session.query(OrderModel).join(PaymentModel).filter(PaymentModel.id == id_payment).first()
        if not order_model:
            return None
        return order_model.to_entity()

    def get_by_id(self, order_id: int) -> Order:
        order_model = self.db_session.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not order_model:
            return None
        return order_model.to_entity()

    def get_all(self, status: Optional[List[str]] = None, customer_id: Optional[int] = None, include_deleted: Optional[bool] = False) -> List[Order]:
        query = self.db_session.query(OrderModel)
    
        if not include_deleted:
            query = query.filter(OrderModel.inactivated_at.is_(None))
        
        if customer_id:
            query = query.filter(OrderModel.id_customer == customer_id)
        
        if status:
            query = query.filter(OrderModel.order_status.has(OrderStatusModel.status.in_(status)))

        if status is None or OrderStatusEnum.ORDER_COMPLETED.status not in status:
            query = query.filter(OrderModel.order_status.has(OrderStatusModel.status != OrderStatusEnum.ORDER_COMPLETED.status))
            
        status_priority = case(
            (OrderStatusModel.status == OrderStatusEnum.ORDER_PAID.status, 1),
            (OrderStatusModel.status == OrderStatusEnum.ORDER_PREPARING.status, 2),
            (OrderStatusModel.status == OrderStatusEnum.ORDER_READY.status, 3),
            (OrderStatusModel.status == OrderStatusEnum.ORDER_COMPLETED.status, 4),
            else_=5
        )

        query = query.join(OrderStatusModel).order_by(status_priority, OrderModel.created_at.asc())
        return [order_model.to_entity() for order_model in query.all()]

    def update(self, order: Order) -> Order:
        if order.id is not None:
            existing_order = self.get_by_id(order.id)
            if existing_order:
                self.identity_map.remove(existing_order)

        order_model = OrderModel.from_entity(order)
        order_model.id_customer = order.id_customer
        order_model.id_employee = order.id_employee
        order_model.order_status = OrderStatusModel.from_entity(order.order_status)
        order_model.status_history = [OrderStatusMovementModel.from_entity(movement) for movement in order.status_history]

        self.db_session.merge(order_model)
        self.db_session.commit()
        return self.get_by_id(order_model.id)

    def delete(self, order: Order) -> None:
        order_model = (
            self.db_session.query(OrderModel)
                .filter(OrderModel.id == order.id)
                .first()
        )
        if order_model:
            self.db_session.delete(order)
            self.db_session.commit()
            self.identity_map.remove(order)
