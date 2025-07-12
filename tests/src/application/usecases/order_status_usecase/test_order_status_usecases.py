import pytest
from unittest.mock import MagicMock

from src.constants.order_status import OrderStatusEnum
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO
from src.core.domain.entities.order_status import OrderStatus
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.application.usecases.order_status_usecase.create_order_status_usecase import CreateOrderStatusUseCase
from src.application.usecases.order_status_usecase.delete_order_status_usecase import DeleteOrderStatusUseCase


class TestOrderStatusUseCases:
    
    @pytest.fixture
    def order_status_gateway(self):
        return MagicMock()
    
    @pytest.fixture
    def order_status(self):
        return OrderStatus(
            status=OrderStatusEnum.ORDER_PENDING.status,
            description="Pedido pendente",
            id=1
        )
    
    def test_create_order_status_usecase(self, order_status_gateway, order_status):
        order_status_gateway.get_by_status.return_value = None
        order_status_gateway.create.return_value = order_status
        create_order_status_usecase = CreateOrderStatusUseCase.build(order_status_gateway)
        
        dto = CreateOrderStatusDTO(
            status=OrderStatusEnum.ORDER_PENDING.status,
            description="Pedido pendente"
        )

        result = create_order_status_usecase.execute(dto)

        assert result.id == 1
        assert result.status == OrderStatusEnum.ORDER_PENDING.status
        assert result.description == "Pedido pendente"
        order_status_gateway.get_by_status.assert_called_once_with(OrderStatusEnum.ORDER_PENDING.status)
        order_status_gateway.create.assert_called_once()
    
    def test_create_order_status_already_exists(self, order_status_gateway, order_status):
        order_status_gateway.get_by_status.return_value = order_status
        create_order_status_usecase = CreateOrderStatusUseCase.build(order_status_gateway)
        
        dto = CreateOrderStatusDTO(
            status=OrderStatusEnum.ORDER_PENDING.status,
            description="Pedido pendente"
        )

        with pytest.raises(EntityDuplicatedException):
            create_order_status_usecase.execute(dto)
    
    def test_create_order_status_reactivate_deleted(self, order_status_gateway, order_status):
        deleted_status = OrderStatus(
            status=OrderStatusEnum.ORDER_PENDING.status,
            description="Original description",
            id=1
        )
        deleted_status.soft_delete()
        
        order_status_gateway.get_by_status.return_value = deleted_status
        order_status_gateway.update.return_value = order_status
        create_order_status_usecase = CreateOrderStatusUseCase.build(order_status_gateway)
        
        dto = CreateOrderStatusDTO(
            status=OrderStatusEnum.ORDER_PENDING.status,
            description="Updated description"
        )

        result = create_order_status_usecase.execute(dto)

        assert result.id == 1
        assert result.status == OrderStatusEnum.ORDER_PENDING.status
        assert not result.is_deleted()
        order_status_gateway.update.assert_called_once()
    
    def test_delete_order_status_usecase_soft_delete(self, order_status_gateway, order_status, monkeypatch):
        monkeypatch.setattr("config.database.DELETE_MODE", "soft")
        order_status_gateway.get_by_id.return_value = order_status
        delete_order_status_usecase = DeleteOrderStatusUseCase.build(order_status_gateway)

        delete_order_status_usecase.execute(1)

        assert order_status.is_deleted()
        order_status_gateway.update.assert_called_once_with(order_status)
    
    def test_delete_order_status_usecase_hard_delete(self, order_status_gateway, order_status, monkeypatch):
        monkeypatch.setattr("config.database.DELETE_MODE", "hard")
        order_status_gateway.get_by_id.return_value = order_status
        delete_order_status_usecase = DeleteOrderStatusUseCase.build(order_status_gateway)
        
        delete_order_status_usecase.execute(1)

        order_status_gateway.update.assert_called_once_with(order_status)
    
    def test_delete_order_status_not_found(self, order_status_gateway):
        order_status_gateway.get_by_id.return_value = None
        delete_order_status_usecase = DeleteOrderStatusUseCase.build(order_status_gateway)
        
        with pytest.raises(EntityNotFoundException):
            delete_order_status_usecase.execute(999)
