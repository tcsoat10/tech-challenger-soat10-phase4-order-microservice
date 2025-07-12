from src.constants.product_category import ProductCategoryEnum
from src.constants.order_status import OrderStatusEnum

ORDER_STATUS_TRANSITIONS = {
    OrderStatusEnum.ORDER_PENDING: OrderStatusEnum.ORDER_WAITING_BURGERS,
    OrderStatusEnum.ORDER_WAITING_BURGERS: OrderStatusEnum.ORDER_WAITING_SIDES,
    OrderStatusEnum.ORDER_WAITING_SIDES: OrderStatusEnum.ORDER_WAITING_DRINKS,
    OrderStatusEnum.ORDER_WAITING_DRINKS: OrderStatusEnum.ORDER_WAITING_DESSERTS,
    OrderStatusEnum.ORDER_WAITING_DESSERTS: OrderStatusEnum.ORDER_READY_TO_PLACE,
    OrderStatusEnum.ORDER_READY_TO_PLACE: OrderStatusEnum.ORDER_PLACED,
    OrderStatusEnum.ORDER_PLACED: OrderStatusEnum.ORDER_PAID,
    OrderStatusEnum.ORDER_PAID: OrderStatusEnum.ORDER_PREPARING,
    OrderStatusEnum.ORDER_PREPARING: OrderStatusEnum.ORDER_READY,
    OrderStatusEnum.ORDER_READY: OrderStatusEnum.ORDER_COMPLETED,
}

STATUS_ALLOWED_ACCESS_ONLY_EMPLOYEE = [
    OrderStatusEnum.ORDER_PAID,
    OrderStatusEnum.ORDER_PREPARING,
    OrderStatusEnum.ORDER_READY,
]

STATUS_ALLOWED_ACCESS_ONLY_CUSTOMER = [
    OrderStatusEnum.ORDER_PENDING,
    OrderStatusEnum.ORDER_WAITING_BURGERS,
    OrderStatusEnum.ORDER_WAITING_SIDES,
    OrderStatusEnum.ORDER_WAITING_DRINKS,
    OrderStatusEnum.ORDER_WAITING_DESSERTS,
    OrderStatusEnum.ORDER_READY_TO_PLACE,
    OrderStatusEnum.ORDER_PLACED,
]

PRODUCT_CATEGORY_TO_ORDER_STATUS = {
    ProductCategoryEnum.BURGERS.name: OrderStatusEnum.ORDER_WAITING_BURGERS,
    ProductCategoryEnum.SIDES.name: OrderStatusEnum.ORDER_WAITING_SIDES,
    ProductCategoryEnum.DRINKS.name: OrderStatusEnum.ORDER_WAITING_DRINKS,
    ProductCategoryEnum.DESSERTS.name: OrderStatusEnum.ORDER_WAITING_DESSERTS,
}

# Define os status de pedido que permitem reversão para um estágio anterior.
# Nestes estados o pedido pode ser retrocedido para ajuste.
ORDER_STATUSES_ALLOWING_REVERSAL_TRANSITIONS = [
    OrderStatusEnum.ORDER_WAITING_SIDES,
    OrderStatusEnum.ORDER_WAITING_DRINKS,
    OrderStatusEnum.ORDER_WAITING_DESSERTS,
    OrderStatusEnum.ORDER_READY_TO_PLACE,
]
