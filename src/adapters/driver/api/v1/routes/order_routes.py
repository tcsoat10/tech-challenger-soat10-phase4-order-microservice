from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Security, status
from dependency_injector.wiring import inject, Provide

from src.constants.order_status import OrderStatusEnum
from src.adapters.driver.api.v1.controllers.order_controller import OrderController
from src.constants.permissions import OrderPermissions
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.containers import Container
from src.core.domain.dtos.order.create_order_dto import CreateOrderDTO


router = APIRouter()


# Criar um pedido
@router.post(
    "/orders",
    response_model=OrderDTO,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_order(    
    dto: CreateOrderDTO,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    return controller.create_order(dto.id_customer)

# Listar produtos com base no status do pedido
@router.get(
    "/orders/{order_id}/products",
    response_model=List[ProductDTO],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_products_by_order_status(
    order_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    return controller.list_products_by_order_status(order_id)

@router.get(
    "/orders/{order_id}",
    response_model=OrderDTO,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_order_by_id(
    order_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    return controller.get_order_by_id(order_id)

# Adicionar item ao pedido
@router.post(
    "/orders/{order_id}/items",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def add_item(
    order_id: int,
    dto: CreateOrderItemDTO,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    controller.add_item(order_id, dto)
    return {"detail": "Item adicionado com sucesso."}

# Remover item do pedido
@router.delete(
    "/orders/{order_id}/items/{item_id}",
    status_code=status.HTTP_200_OK,
)
@inject
async def remove_item(
    order_id: int,
    item_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    controller.remove_item(order_id, item_id)
    return {"detail": "Item removido com sucesso."}

# Atualizar quantidade de item do pedido
@router.put(
    "/orders/{order_id}/items/{item_id}/quantity",
    status_code=status.HTTP_200_OK,
)
@inject
async def change_item_quantity(
    order_id: int,
    order_item_id: int,
    new_quantity: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    controller.change_item_quantity(order_id, order_item_id, new_quantity)
    return {"detail": "Quantidade atualizada com sucesso."}

# Atualizar observação de item do pedido
@router.put(
    "/orders/{order_id}/items/{item_id}/observation",
    status_code=status.HTTP_200_OK,
)
@inject
async def change_item_observation(
    order_id: int,
    item_id: int,
    new_observation: str,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    controller.change_item_observation(order_id, item_id, new_observation)
    return {"detail": "Observação atualizada com sucesso."}

@router.delete(
    "/orders/{order_id}/clear",
    status_code=status.HTTP_200_OK,
)
@inject
async def clear_order(
    order_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    controller.clear_order(order_id)
    return {"detail": "Pedido limpo com sucesso."}

# Listar itens do pedido
@router.get(
    "/orders/{order_id}/items",
    response_model=List[OrderItemDTO],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_order_items(
    order_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    return controller.list_order_items(order_id)

# Cancelar pedido
@router.post(
    "/orders/{order_id}/cancel",
    status_code=status.HTTP_200_OK,
)
@inject
async def cancel_order(
    order_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    controller.cancel_order(order_id)
    return {"detail": "Pedido cancelado com sucesso."}

# Avançar para o próximo passo no pedido
@router.post("/orders/{order_id}/advance")
@inject
async def advance_order_status(
    order_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    return controller.advance_order_status(order_id)

# Retornar ao passo anterior
@router.post(
    "/orders/{order_id}/go-back",
    status_code=status.HTTP_200_OK,
)
@inject
async def go_back(
    order_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    return controller.revert_order_status(order_id)

# Listar todos os pedidos
@router.get(
    "/orders",
    response_model=List[OrderDTO],
    status_code=status.HTTP_200_OK,
)
@inject
async def list_orders(
    status: Optional[List[str]] = Query(
        default=[],
        # example=[s.status for s in OrderStatusEnum],
        description=f"Lista de status dos pedidos para filtrar. Valores válidos: {', '.join([str(s.status) for s in OrderStatusEnum])}"
    ),
    controller: OrderController = Depends(Provide[Container.order_controller]),
):
    return controller.list_orders(status)


@router.get(
    '/orders/{order_id}/status',
    response_model=OrderStatusDTO,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_order_status(
    order_id: int,
    controller: OrderController = Depends(Provide[Container.order_controller])
):
    return controller.get_order_status(order_id)
