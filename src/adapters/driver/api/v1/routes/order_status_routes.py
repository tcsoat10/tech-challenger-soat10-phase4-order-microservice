from typing import List, Optional
from fastapi import APIRouter, Depends, status, Security, Query
from dependency_injector.wiring import inject, Provide

from src.core.auth.dependencies import get_current_user
from src.adapters.driver.api.v1.controllers.order_status_controller import OrderStatusController
from src.core.domain.dtos.order_status.update_order_status_dto import UpdateOrderStatusDTO
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO
from src.constants.permissions import OrderStatusPermissions
from src.core.containers import Container


router = APIRouter()


@router.post(
    "/order_status",
    response_model=OrderStatusDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_CREATE_ORDER_STATUS])],
    include_in_schema=False
)
@inject
def create_order_status(
    dto: CreateOrderStatusDTO,
    controller: OrderStatusController = Depends(Provide[Container.order_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.create_order_status(dto)

@router.get(
    "/order_status/{order_status}/status",
    response_model=OrderStatusDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])]
)
@inject
def get_order_status_by_status(
    order_status: str,
    controller: OrderStatusController = Depends(Provide[Container.order_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_order_status_by_status(status=order_status)

@router.get(
    "/order_status/{order_status_id}/id",
    response_model=OrderStatusDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])]
)
@inject
def get_order_status_by_id(
    order_status_id: int,
    controller: OrderStatusController = Depends(Provide[Container.order_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_order_status_by_id(order_status_id=order_status_id)

@router.get(
    "/order_status",
    response_model=List[OrderStatusDTO],
    dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])]
)
@inject
def get_all_order_status(
    include_deleted: Optional[bool] = Query(False),
    controller: OrderStatusController = Depends(Provide[Container.order_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_all_orders_status(include_deleted=include_deleted)

@router.put(
    "/order_status/{order_status_id}",
    response_model=OrderStatusDTO,
    dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_UPDATE_ORDER_STATUS])],
    include_in_schema=False
)
@inject
def update_order_status(
    order_status_id: int,
    dto: UpdateOrderStatusDTO,
    controller: OrderStatusController = Depends(Provide[Container.order_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.update_order_status(order_status_id, dto)

@router.delete(
    "/order_status/{order_status_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_DELETE_ORDER_STATUS])],
    include_in_schema=False
)
@inject
def delete_order_status(
    order_status_id: int,
    controller: OrderStatusController = Depends(Provide[Container.order_status_controller]),
    user: dict = Security(get_current_user)
):
    controller.delete_order_status(order_status_id)
