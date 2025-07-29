from typing import List

from src.core.domain.entities.order import Order
from src.core.domain.dtos.payment.payment_dto import PaymentDTO
from src.core.domain.dtos.product.product_dto import ProductDTO
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
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.order_usecase.create_order_usecase import CreateOrderUseCase
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.application.usecases.order_usecase.get_order_status_usecase import GetOrderStatusUsecase
from src.core.ports.stock.i_stock_provider_gateway import IStockProviderGateway
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway


class OrderController:

    def __init__(
        self, 
        order_status_gateway: IOrderStatusRepository,        
        order_gateway: IOrderRepository,
        stock_gateway: IStockProviderGateway,
        payment_gateway: IPaymentProviderGateway
    ):
        self.order_status_gateway: IOrderStatusRepository = order_status_gateway
        self.order_gateway: IOrderRepository = order_gateway
        self.stock_gateway: IStockProviderGateway = stock_gateway
        self.payment_gateway: IPaymentProviderGateway = payment_gateway

    def create_order(self, customer: dict) -> OrderDTO:
        create_order_usecase = CreateOrderUseCase.build(self.order_gateway, self.order_status_gateway)
        order = create_order_usecase.execute(customer_id=customer['id'])
        return DTOPresenter.transform(order, OrderDTO)

    def list_products_by_order_status(self, order_id: int, current_user: dict) -> List[ProductDTO]:
        list_products_by_order_status_usecase = ListProductsByOrderStatusUseCase.build(self.order_gateway, self.stock_gateway)
        products = list_products_by_order_status_usecase.execute(order_id, current_user)
        return DTOPresenter.transform_list_from_dict(products, ProductDTO)

    def get_order_by_id(self, order_id: int, current_user: dict) -> OrderDTO:
        order_by_id_usecase = GetOrderByIdUseCase.build(self.order_gateway)
        order = order_by_id_usecase.execute(order_id, current_user)
        return DTOPresenter.transform(order, OrderDTO)

    def add_item(self, order_id: int, order_item_dto: dict, current_user: dict) -> OrderDTO:
        add_order_item_in_order_usecase = AddOrderItemInOrderUseCase.build(self.order_gateway, self.stock_gateway)
        order = add_order_item_in_order_usecase.execute(order_id, order_item_dto, current_user)
        return DTOPresenter.transform(order, OrderDTO)

    def remove_item(self, order_id: int, order_item_id: int, current_user: dict) -> None:
        remove_order_item_in_order_usecase = RemoveOrderItemFromOrderUseCase.build(self.order_gateway)
        remove_order_item_in_order_usecase.execute(order_id, order_item_id)

    def change_item_quantity(self, order_id: int, item_id: int, new_quantity: int, current_user: dict) -> None:
        change_item_quantity_usecase = ChangeItemQuantityUseCase.build(self.order_gateway)
        change_item_quantity_usecase.execute(order_id, item_id, new_quantity, current_user)
  
    def change_item_observation(self, order_id: int, item_id: int, new_observation: str, current_user: dict) -> None:
        change_item_observation_usecase = ChangeItemObservationUseCase.build(self.order_gateway)
        change_item_observation_usecase.execute(order_id, item_id, new_observation, current_user)

    def clear_order(self, order_id: int, current_user: dict) -> None:
        clear_order_usecase = ClearOrderUseCase.build(self.order_gateway, self.order_status_gateway)
        clear_order_usecase.execute(order_id, current_user)

    def list_order_items(self, order_id: int, current_user: dict) -> List[OrderItemDTO]:
        list_order_items_usecase = ListOrderItemsUseCase.build(self.order_gateway)
        order_items = list_order_items_usecase.execute(order_id)
        return DTOPresenter.transform_list(order_items, OrderItemDTO)

    def cancel_order(self, order_id: int, current_user: dict) -> None:
        cancel_order_usecase = CancelOrderUseCase.build(self.order_gateway, self.order_status_gateway)
        cancel_order_usecase.execute(order_id)

    def list_orders(self, status: List[str] = None, current_user: dict = None) -> List[OrderDTO]:
        list_orders_usecase = ListOrdersUseCase.build(self.order_gateway)
        orders = list_orders_usecase.execute(status, current_user)
        return DTOPresenter.transform_list(orders, OrderDTO)

    def advance_order_status(self, order_id: int, current_user: dict) -> OrderDTO | PaymentDTO:
        advance_status_usecase = AdvanceOrderStatusUseCase.build(self.order_gateway, self.order_status_gateway, self.payment_gateway)
        response = advance_status_usecase.execute(order_id, current_user)
        if isinstance(response, Order):
            return DTOPresenter.transform(response, OrderDTO)
        return DTOPresenter.transform_from_dict(response, PaymentDTO)
    
    def revert_order_status(self, order_id: int, current_user: dict) -> OrderDTO:
        revert_status_usecase = RevertOrderStatusUseCase.build(self.order_gateway, self.order_status_gateway)
        order = revert_status_usecase.execute(order_id, current_user)
        return DTOPresenter.transform(order, OrderDTO)
    
    def get_order_status(self, order_id: int, current_user: dict) -> OrderStatusDTO:
        get_order_status_usecase = GetOrderStatusUsecase.build(self.order_gateway)
        order_status = get_order_status_usecase.execute(order_id, current_user)
        return DTOPresenter.transform(order_status, OrderStatusDTO)
