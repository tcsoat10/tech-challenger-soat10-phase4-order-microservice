from typing import List

from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.application.usecases.order_usecase.revert_order_status_usecase import RevertOrderStatusUseCase
from src.application.usecases.order_usecase.advance_order_status_usecase import AdvanceOrderStatusUseCase
from src.application.usecases.order_usecase.list_orders_usecase import ListOrdersUseCase
from src.application.usecases.order_usecase.cancel_order_usecase import CancelOrderUseCase
from src.application.usecases.order_usecase.list_order_item_usecase import ListOrderItemsUseCase
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.application.usecases.order_usecase.clear_order_usecase import ClearOrderUseCase
from src.application.usecases.order_usecase.change_item_observation_usecase import ChangeItemObservationUseCase
from src.application.usecases.order_usecase.change_item_quantity_usecase import ChangeItemQuantityUseCase
from src.application.usecases.order_usecase.remove_order_item_from_order_usecase import RemoveOrderItemFromOrderUseCase
from src.application.usecases.order_usecase.add_order_item_in_order_usecase import AddOrderItemInOrderUseCase
from src.application.usecases.order_usecase.get_order_by_id_usecase import GetOrderByIdUseCase
from src.application.usecases.order_usecase.list_products_by_order_status_usecase import ListProductsByOrderStatusUseCase
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.order_usecase.create_order_usecase import CreateOrderUseCase
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.product.i_product_repository import IProductRepository
from src.application.usecases.order_usecase.get_order_status_usecase import GetOrderStatusUsecase


class OrderController:

    def __init__(
        self, 
        order_status_gateway: IOrderStatusRepository,        
        product_gateway: IProductRepository, 
        order_gateway: IOrderRepository
    ):        
        self.order_status_gateway: IOrderStatusRepository = order_status_gateway
        self.product_gateway: IProductRepository = product_gateway
        self.order_gateway: IOrderRepository = order_gateway
        
    def create_order(self, id_customer: str) -> OrderDTO:
        create_order_usecase = CreateOrderUseCase.build(self.order_gateway, self.order_status_gateway)
        order = create_order_usecase.execute(id_customer)
        return DTOPresenter.transform(order, OrderDTO)

    def list_products_by_order_status(self, order_id: int) -> List[ProductDTO]:
        list_products_by_order_status_usecase = ListProductsByOrderStatusUseCase.build(self.order_gateway, self.product_gateway)
        products = list_products_by_order_status_usecase.execute(order_id)
        return DTOPresenter.transform_list(products, ProductDTO)

    def get_order_by_id(self, order_id: int) -> OrderDTO:
        order_by_id_usecase = GetOrderByIdUseCase.build(self.order_gateway)
        order = order_by_id_usecase.execute(order_id)
        return DTOPresenter.transform(order, OrderDTO)

    def add_item(self, order_id: int, order_item_dto: dict) -> OrderDTO:
        add_order_item_in_order_usecase = AddOrderItemInOrderUseCase.build(self.order_gateway, self.product_gateway)
        order = add_order_item_in_order_usecase.execute(order_id, order_item_dto)
        return DTOPresenter.transform(order, OrderDTO)
        
    def remove_item(self, order_id: int, order_item_id: int) -> None:
        remove_order_item_in_order_usecase = RemoveOrderItemFromOrderUseCase.build(self.order_gateway)
        remove_order_item_in_order_usecase.execute(order_id, order_item_id)
        
    def change_item_quantity(self, order_id: int, item_id: int, new_quantity: int) -> None:
        change_item_quantity_usecase = ChangeItemQuantityUseCase.build(self.order_gateway)
        change_item_quantity_usecase.execute(order_id, item_id, new_quantity)
    
    def change_item_observation(self, order_id: int, item_id: int, new_observation: str) -> None:
        change_item_observation_usecase = ChangeItemObservationUseCase.build(self.order_gateway)
        change_item_observation_usecase.execute(order_id, item_id, new_observation)
        
    def clear_order(self, order_id: int) -> None:
        clear_order_usecase = ClearOrderUseCase.build(self.order_gateway, self.order_status_gateway)
        clear_order_usecase.execute(order_id)

    def list_order_items(self, order_id: int) -> List[OrderItemDTO]:
        list_order_items_usecase = ListOrderItemsUseCase.build(self.order_gateway)
        order_items = list_order_items_usecase.execute(order_id)
        return DTOPresenter.transform_list(order_items, OrderItemDTO)
    
    def cancel_order(self, order_id: int) -> None:
        cancel_order_usecase = CancelOrderUseCase.build(self.order_gateway, self.order_status_gateway)
        cancel_order_usecase.execute(order_id)

    def list_orders(self, status: List[str] = None) -> List[OrderDTO]:
        list_orders_usecase = ListOrdersUseCase.build(self.order_gateway)
        orders = list_orders_usecase.execute(status)
        return DTOPresenter.transform_list(orders, OrderDTO)

    def advance_order_status(self, order_id: int) -> OrderDTO:
        advance_status_usecase = AdvanceOrderStatusUseCase.build(self.order_gateway, self.order_status_gateway)
        order = advance_status_usecase.execute(order_id)
        return DTOPresenter.transform(order, OrderDTO)
    
    def revert_order_status(self, order_id: int) -> OrderDTO:
        revert_status_usecase = RevertOrderStatusUseCase.build(self.order_gateway, self.order_status_gateway)
        order = revert_status_usecase.execute(order_id)
        return DTOPresenter.transform(order, OrderDTO)
    
    def get_order_status(self, order_id: int) -> OrderStatusDTO:
        get_order_status_usecase = GetOrderStatusUsecase.build(self.order_gateway)
        order_status = get_order_status_usecase.execute(order_id)
        return DTOPresenter.transform(order_status, OrderStatusDTO)
