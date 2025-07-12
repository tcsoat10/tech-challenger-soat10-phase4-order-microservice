
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.product.i_product_repository import IProductRepository


class CreateOrderItemUseCase:
    def __init__(self, order_item_gateway: IOrderItemRepository, product_gateway: IProductRepository, order_gateway: IOrderRepository):
        self.order_item_gateway = order_item_gateway
        self.product_gateway = product_gateway
        self.order_gateway = order_gateway
    
    @classmethod
    def build(
        cls,
        order_item_gateway: IOrderItemRepository,
        product_gateway: IProductRepository,
        order_gateway: IOrderRepository
    ) -> 'CreateOrderItemUseCase':
        return cls(order_item_gateway, product_gateway, order_gateway)

    def execute(self, dto: CreateOrderItemDTO) -> OrderItem:
        product = self.product_gateway.get_by_id(dto.product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")

        if not dto.order_id:
            raise EntityNotFoundException(entity_name="Order ID")

        order = self.order_gateway.get_by_id(dto.order_id)
        if not order:
            raise EntityNotFoundException(entity_name="Order")

        order_item = OrderItem(
            order=order,
            product=product,
            quantity=dto.quantity,
            observation=dto.observation,
        )

        order_item = self.order_item_gateway.create(order_item)
        return order_item
