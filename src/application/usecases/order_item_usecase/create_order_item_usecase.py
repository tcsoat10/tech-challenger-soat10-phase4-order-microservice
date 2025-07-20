
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.stock.i_stock_provider_gateway import IStockProviderGateway


class CreateOrderItemUseCase:
    def __init__(
            self,
            order_item_gateway: IOrderItemRepository,
            order_gateway: IOrderRepository,
            stock_gateway: IStockProviderGateway
    ):
        self.order_item_gateway = order_item_gateway
        self.order_gateway = order_gateway
        self.stock_gateway = stock_gateway

    @classmethod
    def build(
        cls,
        order_item_gateway: IOrderItemRepository,
        order_gateway: IOrderRepository,
        stock_gateway: IStockProviderGateway
    ) -> 'CreateOrderItemUseCase':
        return cls(order_item_gateway, order_gateway, stock_gateway)

    def execute(self, dto: CreateOrderItemDTO) -> OrderItem:
        product = self.stock_gateway.get_product_by_id(dto.product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")

        if not dto.order_id:
            raise EntityNotFoundException(entity_name="Order ID")

        order = self.order_gateway.get_by_id(dto.order_id)
        if not order:
            raise EntityNotFoundException(entity_name="Order")

        order_item = OrderItem(
            order=order,
            product_id=product['id'],
            product_name=product['name'],
            product_price=product['price'],
            product_category_name=product.get('category_name', ''),
            quantity=dto.quantity,
            observation=dto.observation,
        )

        order_item = self.order_item_gateway.create(order_item)
        return order_item
