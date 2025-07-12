from enum import Enum

from src.core.exceptions.entity_not_found_exception import EntityNotFoundException

class OrderStatusEnum(Enum):
    ORDER_PENDING = ("order_pending", "The order is pending.") # Order created
    ORDER_WAITING_BURGERS = ("order_waiting_burgers", "Waiting for a burger.") # Order waiting for a sandwiches
    ORDER_WAITING_SIDES = ("order_waiting_sides", "Waiting for a side dish.") # Order waiting for a side dishes
    ORDER_WAITING_DRINKS = ("order_waiting_drinks", "Waiting for a drink.") # Order waiting for a drinks
    ORDER_WAITING_DESSERTS = ("order_waiting_desserts", "Waiting for a dessert.") # Order waiting for a desserts
    ORDER_READY_TO_PLACE = ("order_ready_to_place", "The order is ready to be placed.") # Order ready to confirm by the customer
    ORDER_PLACED = ("order_placed", "The customer has placed the order.") # Order confirmed by the customer
    ORDER_PAID = ("order_paid", "The customer has paid the order.") # Order paid by the customer
    ORDER_PREPARING = ("order_preparing", "The order is being prepared.") # Order being prepared by the staff
    ORDER_READY = ("order_ready", "The order is ready for pickup at the counter.") # Order ready for pickup
    ORDER_COMPLETED = ("order_completed", "The customer has received the order.") # Order received by the customer
    ORDER_CANCELLED = ("order_cancelled", "The order was cancelled by the customer or staff.") # Order cancelled by the customer or staff

    @property
    def status(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    @classmethod
    def values_and_descriptions(cls):
        return [{"status": member.status, "description": member.description} for member in cls]
    
    @classmethod
    def from_status(cls, status: str) -> "OrderStatusEnum":
        for member in cls:
            if member.status == status:
                return member

        raise EntityNotFoundException(status)
