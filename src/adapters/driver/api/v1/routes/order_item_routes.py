from fastapi import APIRouter, Depends, status, Security
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.order_item_controller import OrderItemController
from config.database import get_db
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.constants.permissions import OrderItemPermissions
from src.core.containers import Container


router = APIRouter()


@router.post(
        "/order-items",
        response_model=OrderItemDTO,
        status_code=status.HTTP_201_CREATED,
)
@inject
def create_order_item(
    dto: CreateOrderItemDTO,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
):
    return controller.create_order_item(dto)

@router.get(
        "/order-items/{order_item_id}/id",
        response_model=OrderItemDTO,
        status_code=status.HTTP_200_OK,
)
@inject
def get_order_item_by_id(
    order_item_id: int,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
):
    return controller.get_order_item_by_id(order_item_id)

@router.get(
        "/order-items",
        response_model=list[OrderItemDTO],
)
@inject
def get_all_order_items(
    include_deleted: bool = False,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
):
    return controller.get_all_order_items(include_deleted)

@router.put(
        "/order-items/{order_item_id}",
        response_model=OrderItemDTO,
)
@inject
def update_order_item(
    order_item_id: int,
    dto: UpdateOrderItemDTO,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
):
    return controller.update_order_item(order_item_id, dto)

@router.delete(
    "/order-items/{order_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
def delete_order_item(
    order_item_id: int,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
):
    controller.delete_order_item(order_item_id)
