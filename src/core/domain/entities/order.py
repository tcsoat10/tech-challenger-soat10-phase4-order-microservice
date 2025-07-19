from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import uuid

from src.core.domain.entities.order_status_movement import OrderStatusMovement
from src.constants.order_transition import PRODUCT_CATEGORY_TO_ORDER_STATUS, ORDER_STATUS_TRANSITIONS, ORDER_STATUSES_ALLOWING_REVERSAL_TRANSITIONS
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.constants.product_category import ProductCategoryEnum
from src.core.domain.entities.order_status import OrderStatus
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from .base_entity import BaseEntity


class Order(BaseEntity):
    
    def __init__(
        self,
        id_customer: str = None,
        id_employee: str = None,
        order_status: Optional[OrderStatus] = None,
        order_items: List[OrderItem] = [],
        status_history: Optional[List[OrderStatusMovement]] = [],
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        inactivated_at: Optional[datetime] = None,
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self.id_customer = id_customer
        self.id_employee = id_employee
        self.order_status = order_status
        self.order_items = order_items
        self.status_history = status_history
        
        initial_status = OrderStatusMovement(
            order=self,
            old_status=None,
            new_status=OrderStatusEnum.ORDER_PENDING.status,
            changed_at=datetime.now(timezone.utc),
            changed_by="System",
        )
        self.status_history.append(initial_status)
        
    @property
    def id_customer(self) -> str:
        return self._customer

    @id_customer.setter
    def id_customer(self, value: str) -> None:
        self._customer = value

    @property
    def id_employee(self) -> Optional[str]:
        return self._employee

    @id_employee.setter
    def id_employee(self, value: Optional[str]) -> None:
        self._employee = value

    @property
    def order_status(self) -> OrderStatus:
        return self._order_status

    @order_status.setter
    def order_status(self, value: OrderStatus) -> None:
        self._order_status = value

    @property
    def order_items(self) -> List[OrderItem]:
        return self._order_items

    @order_items.setter
    def order_items(self, value: List[OrderItem]) -> None:
        self._order_items = value

    @property
    def status_history(self) -> List[OrderStatusMovement]:
        return self._status_history

    @status_history.setter
    def status_history(self, value: List[OrderStatusMovement]) -> None:
        self._status_history = value

    '''
    @property
    def customer_name(self) -> Optional[str]:
        if self.customer and self.customer.person:
            return self.customer.person.name
        
        return None

    @property
    def employee_name(self) -> Optional[str]:
        if self.employee and self.employee.person:
            return self.employee.person.name
        
        return None
    '''

    @property
    def total(self) -> float:
        if not hasattr(self, "_total"):
            self._total = sum(item.total for item in self.order_items)
        return self._total
        
    '''
    @property
    def is_paid(self) -> bool:
        if self.payment:
            return self.payment.is_completed()
        return False
    '''

    def _validate_status(self, valid_statuses: List[OrderStatusEnum], action: str) -> None:
        '''
        Validates if the current status of the order is in the list of valid statuses.

        :param valid_statuses: List of valid statuses.
        '''
        if self.order_status.status not in [order_status.status for order_status in valid_statuses]:
            raise BadRequestException(f"O pedido não está em um estado válido para {action}.")

    def _validate_category_for_status(self, category_name: str) -> None:
        '''
        Validates if the category of the item is valid for the current status of the order.

        The correct order is:
        - Burgers
        - Sides
        - Drinks
        - Desserts

        :param category: The category of the item.
        '''
        expected_status = PRODUCT_CATEGORY_TO_ORDER_STATUS.get(category_name)
        if not expected_status:
            raise BadRequestException(f"Categoria inválida: {category_name}.")

        if self.order_status.status != expected_status.status:
            raise BadRequestException(
                f"Não é possível adicionar itens da categoria '{category_name}' no status atual "
                f"'{self.order_status.status}'."
            )
        
    def _sort_order_items(self) -> None:
        '''
        Sorts the order items based on the category sequence.

        The category sequence is defined in the `category_sequence`.
        '''
        category_sequence = [
            ProductCategoryEnum.BURGERS.name,
            ProductCategoryEnum.SIDES.name,
            ProductCategoryEnum.DRINKS.name,
            ProductCategoryEnum.DESSERTS.name,
        ]
        
        categorized_items = {category: [] for category in category_sequence}
        for item in self.order_items:
            category_name = item.product_category_name
            if category_name in categorized_items:
                categorized_items[category_name].append(item)
            else:
                raise BadRequestException(f"Item com categoria inválida: {item.product.name}")

        sorted_items = []
        for name in category_sequence:
            sorted_items.extend(categorized_items[name])

        self.order_items = sorted_items

    def _record_status_change(self, new_status: OrderStatus, changed_by: str) -> None:
        '''
        Records a status change in the status history.

        :param new_status: The new status of the order.
        :param changed_by: The name of the user who changed the status.
        '''
        
        order_snapshot = { "id": self.id }
        if self.id_employee:
            order_snapshot["id_employee"] = self.id_employee
            #order_snapshot["employee_name"] = self.employee.person.name
        
        if self.id_customer:    
            order_snapshot["id_customer"] = self.id_customer
            #order_snapshot["customer_name"] = self.customer.person.name

        '''
        if self.payment:
            order_snapshot["payment_id"] = self.payment.id
            order_snapshot["transaction_id"] = self.payment.transaction_id
            order_snapshot["qr_code"] = self.payment.qr_code
            order_snapshot["amount"] = self.payment.amount
        '''

        order_snapshot["current_status"] = self.order_status.status
        order_snapshot["total"] = self.total
        
        if self.order_items and self.order_status.status in [OrderStatusEnum.ORDER_READY_TO_PLACE.status, OrderStatusEnum.ORDER_PLACED.status]:
            order_snapshot["order_items"] = [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.product_price,
                    "total": item.total,
                    "observation": item.observation,
                }
                for item in self.order_items
            ]
        
        movement = OrderStatusMovement(
            order=self,
            order_snapshot=order_snapshot,
            old_status=self.order_status.status,
            new_status=new_status.status,
            changed_at=datetime.now(timezone.utc),
            changed_by=changed_by,
        )
        self.status_history.append(movement)

    def add_item(self, item: OrderItem) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values()], "adicionar itens")
        self._validate_category_for_status(item.product_category_name)

        self.order_items.append(item)
        self._sort_order_items()

    def remove_item(self, order_item: OrderItem) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values()], "remover itens")
        if order_item.quantity > 1:
            order_item.quantity -= 1
        else:    
            self.order_items.remove(order_item)

    def change_item_quantity(self, item: OrderItem, new_quantity: int) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values()], "alterar a quantidade de itens")

        if new_quantity <= 0:
            raise BadRequestException("A quantidade do item deve ser maior que zero.")

        item.quantity = new_quantity

    def change_item_observation(self, item: OrderItem, new_observation: str) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values()], "alterar a observação do item")
        item.observation = new_observation

    def clear_order(self, order_status_repository: IOrderStatusRepository) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values(), OrderStatusEnum.ORDER_READY_TO_PLACE], "limpar o pedido")
        self.order_items = []

        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_BURGERS.status)

    def list_order_items(self) -> List[OrderItem]:
        return self.order_items

    def cancel_order(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        self._validate_status(
            [
                OrderStatusEnum.ORDER_PENDING,
                *PRODUCT_CATEGORY_TO_ORDER_STATUS.values(),
                OrderStatusEnum.ORDER_READY_TO_PLACE,
                OrderStatusEnum.ORDER_PLACED
            ], "cancelar o pedido"
        )

        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_CANCELLED.status)
        owner = movement_owner or self.id_customer or "Cliente Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_waiting_burguer(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING.status, OrderStatusEnum.ORDER_WAITING_SIDES.status]:
            raise BadRequestException("Não é possível selecionar sanduíches neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_BURGERS.status)

    def set_status_waiting_sides(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_WAITING_BURGERS.status, OrderStatusEnum.ORDER_WAITING_DRINKS.status]:
            raise BadRequestException("Não é possível selecionar acompanhamentos neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_SIDES.status)

    def set_status_waiting_drinks(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_WAITING_SIDES.status, OrderStatusEnum.ORDER_WAITING_DESSERTS.status]:
            raise BadRequestException("Não é possível selecionar bebidas neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_DRINKS.status)
    
    def set_status_waiting_desserts(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_WAITING_DRINKS.status, OrderStatusEnum.ORDER_READY_TO_PLACE.status]:
            raise BadRequestException("Não é possível selecionar sobremesas neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_DESSERTS.status)
    
    def set_status_ready_to_place(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_WAITING_DESSERTS.status:
            raise BadRequestException("Não é possível confirmar o pedido neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_READY_TO_PLACE.status)

    def set_status_placed(
            self,
            order_status_repository: IOrderStatusRepository,
            movement_owner: Optional[str] = None,
        ) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_READY_TO_PLACE.status:
            raise BadRequestException("Não é possível finalizar o pedido neste momento.")

        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_PLACED.status)
        #owner = movement_owner or self.customer_name or "Cliente Anônimo"
        owner = movement_owner or self.id_customer or "Cliente Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_paid(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_PLACED.status:
            raise BadRequestException("Não é possível confirmar o pagamento neste momento.")
        
        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        owner = "System"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_preparing(self, order_status_repository: IOrderStatusRepository, employee: str, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_PAID.status:
            raise BadRequestException("Não é possível preparar o pedido neste momento.")

        if not employee:
            raise BadRequestException("É necessário um funcionário para preparar o pedido.")
        
        self.id_employee = employee
        self.employee = employee

        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_PREPARING.status)
        owner = movement_owner or self.id_employee or "Funcionário Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_ready(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_PREPARING.status:
            raise BadRequestException("Não é possível finalizar o pedido neste momento.")
        
        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_READY.status)
        owner = movement_owner or self.id_employee or "Funcionário Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_completed(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_READY.status:
            raise BadRequestException("Não é possível completar o pedido neste momento.")
        
        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_COMPLETED.status)
        owner = movement_owner or self.id_employee or "Funcionário Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    
    def advance_order_status(
        self,
        order_status_repository: IOrderStatusRepository,
        movement_owner: Optional[str] = None,
        employee: Optional[str] = None,
    ) -> None:
        '''
        Advances the order to the next step based on the current status.

        :param movement_owner: The name of the user who is advancing the order.
        :param employee: The employee responsible for preparing the order. this parameter is required when the order is being prepared.
        '''

        current_status = OrderStatusEnum.from_status(self.order_status.status)

        if current_status not in ORDER_STATUS_TRANSITIONS:
            raise BadRequestException(f"O estado atual {current_status.status} não permite transições.")

        expected_next_status = ORDER_STATUS_TRANSITIONS[current_status]

        if expected_next_status == OrderStatusEnum.ORDER_WAITING_BURGERS:
            self.set_status_waiting_burguer(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_WAITING_SIDES:
            self.set_status_waiting_sides(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_WAITING_DRINKS:
            self.set_status_waiting_drinks(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_WAITING_DESSERTS:
            self.set_status_waiting_desserts(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_READY_TO_PLACE:
            self.set_status_ready_to_place(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_PLACED:
            self.set_status_placed(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_PAID:
            self.set_status_paid(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_PREPARING:
            self.set_status_preparing(order_status_repository, employee, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_READY:
            self.set_status_ready(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_COMPLETED:
            self.set_status_completed(order_status_repository, movement_owner)
        else:
            raise BadRequestException(f"Status não suportado: {expected_next_status.status}")

    def revert_order_status(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        '''
        Reverts the order to the previous status.
        
        This operation is only allowed for statuses:
        - ORDER_WAITING_SIDES
        - ORDER_WAITING_DRINKS
        - ORDER_WAITING_DESSERTS
        - ORDER_READY_TO_PLACE

        Raises:
        - BadRequestException: If the current status does not allow going back.
        - BadRequestException: If the previous status cannot be determined.
        '''

        current_status = OrderStatusEnum.from_status(self.order_status.status)
        if current_status not in ORDER_STATUSES_ALLOWING_REVERSAL_TRANSITIONS:
            raise BadRequestException(
                f"O status atual '{current_status.status}' não permite voltar."
            )

        previous_status = None
        for status, next_status in ORDER_STATUS_TRANSITIONS.items():
            if next_status == current_status:
                previous_status = status
                break

        if not previous_status:
            raise BadRequestException("Não foi possível determinar o status anterior.")

        if previous_status == OrderStatusEnum.ORDER_WAITING_BURGERS:
            self.set_status_waiting_burguer(order_status_repository, movement_owner)
        elif previous_status == OrderStatusEnum.ORDER_WAITING_SIDES:
            self.set_status_waiting_sides(order_status_repository, movement_owner)
        elif previous_status == OrderStatusEnum.ORDER_WAITING_DRINKS:
            self.set_status_waiting_drinks(order_status_repository, movement_owner)
        elif previous_status == OrderStatusEnum.ORDER_WAITING_DESSERTS:
            self.set_status_waiting_desserts(order_status_repository, movement_owner)
        elif previous_status == OrderStatusEnum.ORDER_READY_TO_PLACE:
            self.set_status_ready_to_place(order_status_repository, movement_owner)
        else:
            raise BadRequestException(f"Transição de status não suportada: {previous_status.status}")
    
    def is_customer_owner(self, customer_id: int):
        return self.customer.id == customer_id
        
    def has_payment(self) -> bool:
        return self.payment is not None

    def is_in_placed_status(self):
        return self.order_status.status == OrderStatusEnum.ORDER_PLACED.status
    
    def validate_payment(self, current_user: dict) -> Optional[Dict[str, Any]]:
        """
        Validates if the order is eligible for payment processing.
        Returns payment data if a payment already exists and is pending or completed.
        Raises exceptions if validation fails.
        """
        current_user_id = int(current_user["person"]["id"])    
        if not self.is_customer_owner(current_user_id):
            raise BadRequestException("Você não tem permissão para acessar este pedido.")

        if self.has_payment():
            if self.payment.is_pending() or self.payment.is_completed():
                return {
                    "payment_id": self.payment.id,
                    "transaction_id": self.payment.transaction_id,
                    "qr_code_link": self.payment.qr_code,
                }

        if not self.is_in_placed_status():
            raise BadRequestException("Não é possível processar o pagamento neste momento.")

        return None

    def prepare_payment_data(self, webhook_url: str) -> Dict[str, Any]:
        return {
            "external_reference": f"order-{self.id}-{uuid.uuid4()}",
            "notification_url": f"{webhook_url}/api/v1/webhook/payment",
            "total_amount": self.total,
            "items": [
                {
                    "category": order_item.product.category.name,
                    "title": order_item.product.name,
                    "description": order_item.product.description,
                    "quantity": order_item.quantity,
                    "unit_measure": "unit",
                    "unit_price": order_item.product.price,
                    "total_amount": order_item.total
                }
                for order_item in self.order_items
            ],
            "title": f"Compra do pedido {self.id}",
            "description": f"Compra do pedido {self.id}"
        }


__all__ = ['Order']
