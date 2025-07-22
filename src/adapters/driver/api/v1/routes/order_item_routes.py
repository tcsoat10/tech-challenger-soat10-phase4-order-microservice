from fastapi import APIRouter, Depends, status, Security
from dependency_injector.wiring import inject, Provide

from src.core.auth.dependencies import get_current_user
from src.adapters.driver.api.v1.controllers.order_item_controller import OrderItemController
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
    dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_CREATE_ORDER_ITEM])]
)
@inject
def create_order_item(
    dto: CreateOrderItemDTO,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    return controller.create_order_item(dto)

@router.get(
    "/order-items/{order_item_id}/id",
    response_model=OrderItemDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_VIEW_ORDER_ITEMS])]
)
@inject
def get_order_item_by_id(
    order_item_id: int,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_order_item_by_id(order_item_id)

@router.get(
    "/order-items",
    response_model=list[OrderItemDTO],
    dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_VIEW_ORDER_ITEMS])]
)
@inject
def get_all_order_items(
    include_deleted: bool = False,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_all_order_items(include_deleted)

@router.put(
    "/order-items/{order_item_id}",
    response_model=OrderItemDTO,
    dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_UPDATE_ORDER_ITEM])]
)
@inject
def update_order_item(
    order_item_id: int,
    dto: UpdateOrderItemDTO,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    return controller.update_order_item(order_item_id, dto)

@router.delete(
    "/order-items/{order_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_DELETE_ORDER_ITEM])]
)
@inject
def delete_order_item(
    order_item_id: int,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    controller.delete_order_item(order_item_id)
