
from typing import List, Optional

from src.application.usecases.order_item_usecase.delete_order_item_usecase import DeleteOrderItemUseCase
from src.application.usecases.order_item_usecase.update_order_item_usecase import UpdateOrderItemUseCase
from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.application.usecases.order_item_usecase.get_all_order_items_usecase import GetAllOrderItemsUsecase
from src.application.usecases.order_item_usecase.get_order_item_by_id import GetOrderItemByIdUseCase
from src.application.usecases.order_item_usecase.create_order_item_usecase import CreateOrderItemUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.product.i_product_repository import IProductRepository

class OrderItemController:

    def __init__(self, order_item_gateway: IOrderItemRepository, product_gateway: IProductRepository, order_gateway: IOrderRepository):
        self.order_item_gateway: IOrderItemRepository = order_item_gateway
        self.product_gateway: IProductRepository = product_gateway
        self.order_gateway: IOrderRepository = order_gateway
        
    def create_order_item(self, dto: CreateOrderItemDTO) -> OrderItemDTO:
        create_order_item_usecase = CreateOrderItemUseCase.build(self.order_item_gateway, self.product_gateway, self.order_gateway)
        order_item = create_order_item_usecase.execute(dto)
        return DTOPresenter.transform(order_item, OrderItemDTO)

    def get_order_item_by_id(self, order_item_id: int) -> OrderItemDTO:
        order_item_by_id = GetOrderItemByIdUseCase.build(self.order_item_gateway)
        order_item = order_item_by_id.execute(order_item_id)
        return DTOPresenter.transform(order_item, OrderItemDTO)

    def get_all_order_items(self, include_deleted: Optional[bool] = False) -> List[OrderItemDTO]:
        order_items_usecase = GetAllOrderItemsUsecase.build(self.order_item_gateway)
        order_items = order_items_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(order_items, OrderItemDTO)

    def update_order_item(self, order_item_id: int, dto: UpdateOrderItemDTO) -> OrderItemDTO:
        update_order_item_usecase = UpdateOrderItemUseCase.build(self.order_item_gateway, self.product_gateway)
        order_item = update_order_item_usecase.execute(order_item_id, dto)
        return DTOPresenter.transform(order_item, OrderItemDTO)
    
    def delete_order_item(self, order_item_id: int) -> None:
        delete_order_item_usecase = DeleteOrderItemUseCase.build(self.order_item_gateway)
        delete_order_item_usecase.execute(order_item_id)
