
from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.stock.i_stock_provider_gateway import IStockProviderGateway


class UpdateOrderItemUseCase:
    
    def __init__(self, order_item_gateway: IOrderItemRepository, stock_gateway: IStockProviderGateway):
        self.order_item_gateway = order_item_gateway
        self.stock_gateway = stock_gateway
        
    @classmethod
    def build(
        cls,
        order_item_gateway: IOrderItemRepository,
        stock_gateway: IStockProviderGateway
    ) -> 'UpdateOrderItemUseCase':
        return cls(order_item_gateway, stock_gateway)
    
    def execute(self, order_item_id: int, dto: UpdateOrderItemDTO) -> OrderItem:
        order_item = self.order_item_gateway.get_by_id(order_item_id)
        if not order_item:
            raise EntityNotFoundException(entity_name="Order Item")

        product = self.stock_gateway.get_product_by_id(dto.product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")

        order_item.product_id = product['id']
        order_item.quantity = dto.quantity
        order_item.observation = dto.observation

        order_item = self.order_item_gateway.update(order_item)
        return order_item
