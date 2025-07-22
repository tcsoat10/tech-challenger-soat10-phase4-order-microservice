from datetime import datetime
import pytest
from pycpfcnpj import gen
from unittest.mock import patch

from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from src.constants.product_category import ProductCategoryEnum

from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO

from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.adapters.driven.providers.stock_provider.stock_microservice_gateway import StockMicroserviceGateway
from src.adapters.driven.providers.payment_provider.payment_provider_gateway import PaymentProviderGateway

from src.application.usecases.order_usecase.create_order_usecase import CreateOrderUseCase
from src.application.usecases.order_usecase.add_order_item_in_order_usecase import AddOrderItemInOrderUseCase
from src.application.usecases.order_usecase.list_orders_usecase import ListOrdersUseCase
from src.application.usecases.order_usecase.list_order_item_usecase import ListOrderItemsUseCase
from src.application.usecases.order_usecase.remove_order_item_from_order_usecase import RemoveOrderItemFromOrderUseCase
from src.application.usecases.order_usecase.change_item_quantity_usecase import ChangeItemQuantityUseCase
from src.application.usecases.order_usecase.clear_order_usecase import ClearOrderUseCase
from src.application.usecases.order_usecase.advance_order_status_usecase import AdvanceOrderStatusUseCase
from src.application.usecases.order_usecase.revert_order_status_usecase import RevertOrderStatusUseCase
from src.application.usecases.order_usecase.list_products_by_order_status_usecase import ListProductsByOrderStatusUseCase
from src.application.usecases.order_usecase.get_order_status_usecase import GetOrderStatusUsecase


class TestOrderUseCases:
    @pytest.fixture(autouse=True)
    def setup(self, db_session, populate_order_status):
        self.order_gateway = OrderRepository(db_session)
        self.order_status_gateway = OrderStatusRepository(db_session)
        self.stock_gateway = StockMicroserviceGateway()
        self.payment_gateway = PaymentProviderGateway()  # <-- nome correto

        self.create_order_usecase = CreateOrderUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway,
        )
        
        self.add_order_item_usecase = AddOrderItemInOrderUseCase.build(
            order_gateway=self.order_gateway,
            stock_gateway=self.stock_gateway,
        )
        
        self.list_orders_usecase = ListOrdersUseCase.build(order_gateway=self.order_gateway)
        
        self.list_order_items_usecase = ListOrderItemsUseCase.build(order_gateway=self.order_gateway)
        
        self.remove_order_item_usecase = RemoveOrderItemFromOrderUseCase.build(order_gateway=self.order_gateway)
        
        self.change_item_quantity_usecase = ChangeItemQuantityUseCase.build(order_gateway=self.order_gateway)
        
        self.clear_order_usecase = ClearOrderUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway
        )
        
        self.advance_order_status_usecase = AdvanceOrderStatusUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway,
            payment_gateway=self.payment_gateway
        )
        
        self.revert_order_status_usecase = RevertOrderStatusUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway
        )
        
        self.list_products_by_order_status_usecase = ListProductsByOrderStatusUseCase.build(
            order_gateway=self.order_gateway,
            stock_provider_gateway=self.stock_gateway
        )

        self.get_order_status_usecase = GetOrderStatusUsecase.build(order_gateway=self.order_gateway)
        
        self._create_test_data()
    
    def _create_test_data(self):        
        self.test_customer = 'customer'
        self.burger_order_item = {
            "product_id": 1,
            "quantity": 2,
            "observation": "No pickles"
        }

    @pytest.fixture
    def customer_user(self):
        return {
            "profile": {"name": self.test_customer},
            "person": {"id": "1"}
        }

    def test_create_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        
        assert order.id is not None
        assert order.id_customer == customer_user['person']['id']
        assert order.order_status.status == OrderStatusEnum.ORDER_PENDING.status
    '''
    def test_create_order_when_open_order_exists(self, customer_user):
        self.create_order_usecase.execute(customer=customer_user)
        
        with pytest.raises(BadRequestException, match="Já existe um pedido em aberto para este cliente"):
            self.create_order_usecase.execute(customer=customer_user)
    '''

    def test_list_orders_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        self.order_gateway.update(order)
        
        orders = self.list_orders_usecase.execute(current_user=customer_user)
        
        assert len(orders) == 1
        assert orders[0].id == order.id
    
    def test_advance_order_status_to_waiting_burgers(self, customer_user):
        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        updated_order = self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
    
    @patch("src.adapters.driven.providers.stock_provider.stock_microservice_gateway.StockMicroserviceGateway.get_product_by_id")
    def test_add_order_item_in_order_usecase(self, mock_get_product_by_id, customer_user):
        mock_get_product_by_id.return_value = {
            "id": "1",
            "name": "Burger",
            "description": "Delicious beef burger",
            "category": {"id": "1", "name": ProductCategoryEnum.BURGERS.name},
            "price": 6.0
        }

        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=2,
            observation="No pickles"
        )
        
        updated_order = self.add_order_item_usecase.execute(
            order_id=order.id,
            order_item_dto=order_item_dto,
            current_user=customer_user
        )
        
        assert len(updated_order.order_items) == 1
        assert updated_order.order_items[0].product_id == self.burger_order_item['product_id']
        assert updated_order.order_items[0].quantity == 2
        assert updated_order.order_items[0].observation == "No pickles"

    @patch("src.adapters.driven.providers.stock_provider.stock_microservice_gateway.StockMicroserviceGateway.get_product_by_id")
    def test_list_order_items_usecase(self, mock_get_product_by_id, customer_user):
        mock_get_product_by_id.return_value = {
            "id": "1",
            "name": "Burger",
            "description": "Delicious beef burger",
            "category": {"id": "1", "name": ProductCategoryEnum.BURGERS.name},
            "price": 6.0
        }

        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=2,
            observation="No pickles"
        )

        self.add_order_item_usecase.execute(order_id=order.id, order_item_dto=order_item_dto, current_user=customer_user)

        order_items = self.list_order_items_usecase.execute(order_id=order.id)
        
        assert len(order_items) == 1
        assert order_items[0].product_id == self.burger_order_item['product_id']
        assert order_items[0].quantity == 2

    @patch("src.adapters.driven.providers.stock_provider.stock_microservice_gateway.StockMicroserviceGateway.get_product_by_id")
    def test_change_item_quantity_usecase(self, mock_get_product_by_id, customer_user):
        mock_get_product_by_id.return_value = {
            "id": "1",
            "name": "Burger",
            "description": "Delicious beef burger",
            "category": {"id": "1", "name": ProductCategoryEnum.BURGERS.name},
            "price": 6.0
        }

        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=2,
            observation="No pickles"
        )

        updated_order = self.add_order_item_usecase.execute(order_id=order.id, order_item_dto=order_item_dto, current_user=customer_user)

        order_item_id = updated_order.order_items[0].id

        self.change_item_quantity_usecase.execute(order_id=order.id, order_item_id=order_item_id, new_quantity=3, current_user=customer_user)

        order_items = self.list_order_items_usecase.execute(order_id=order.id)
        
        assert order_items[0].quantity == 3

    @patch("src.adapters.driven.providers.stock_provider.stock_microservice_gateway.StockMicroserviceGateway.get_product_by_id")
    def test_remove_order_item_from_order_usecase(self, mock_get_product_by_id, customer_user):
        mock_get_product_by_id.return_value = {
            "id": "1",
            "name": "Burger",
            "description": "Delicious beef burger",
            "category": {"id": "1", "name": ProductCategoryEnum.BURGERS.name},
            "price": 6.0
        }

        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=1,
            observation="No pickles"
        )

        updated_order = self.add_order_item_usecase.execute(order_id=order.id, order_item_dto=order_item_dto, current_user=customer_user)

        order_item_id = updated_order.order_items[0].id

        self.remove_order_item_usecase.execute(order_id=order.id, order_item_id=order_item_id)

        order_items = self.list_order_items_usecase.execute(order_id=order.id)
        
        assert len(order_items) == 0
    
    @patch("src.adapters.driven.providers.stock_provider.stock_microservice_gateway.StockMicroserviceGateway.get_product_by_id")
    def test_clear_order_usecase(self, mock_get_product_by_id, customer_user):
        mock_get_product_by_id.return_value = {
            "id": "1",
            "name": "Burger",
            "description": "Delicious beef burger",
            "category": {"id": "1", "name": ProductCategoryEnum.BURGERS.name},
            "price": 6.0
        }

        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=2,
            observation="No pickles"
        )

        self.add_order_item_usecase.execute(order_id=order.id, order_item_dto=order_item_dto, current_user=customer_user)

        self.clear_order_usecase.execute(order_id=order.id, current_user=customer_user)

        order_items = self.list_order_items_usecase.execute(order_id=order.id)

        assert len(order_items) == 0
    
    def test_revert_order_status_usecase_when_order_is_waiting_burgers_and_return_error(self, customer_user):
        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        updated_order = self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
        
        with pytest.raises(BadRequestException) as exc:
            self.revert_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        assert exc.value.args[0] == "O status atual 'order_waiting_burgers' não permite voltar."
        
    def test_revert_order_status_usecase_when_order_is_waiting_side_dishes_and_return_success(self, customer_user):
        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        updated_order = self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)
        updated_order = self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_SIDES.status

        self.revert_order_status_usecase.execute(order_id=order.id, current_user=customer_user)
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
    
    @patch("src.adapters.driven.providers.stock_provider.stock_microservice_gateway.StockMicroserviceGateway.get_products_by_category_id")
    @patch("src.adapters.driven.providers.stock_provider.stock_microservice_gateway.StockMicroserviceGateway.get_category_by_name")
    def test_list_products_by_order_status_usecase(self, mock_get_category_by_name, mock_get_products_by_category_id, customer_user):
        mock_get_category_by_name.return_value = {
            "id": "1",
            "name": ProductCategoryEnum.BURGERS.name,
            "description": ProductCategoryEnum.BURGERS.description
        }
        
        mock_get_products_by_category_id.return_value = mock_get_products_by_category_id.return_value = [{
            "id": "1",
            "name": "Burger",
            "description": "Delicious beef burger",
            "category": {"id": "1", "name": ProductCategoryEnum.BURGERS.name},
            "price": 6.0
        }]

        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        products = self.list_products_by_order_status_usecase.execute(order_id=order.id, current_user=customer_user)

        assert len(products) == 1
        assert products[0]['id'] == f"{self.burger_order_item['product_id']}"
    
    def test_access_non_existent_order(self, customer_user):
        with pytest.raises(EntityNotFoundException):
            self.list_order_items_usecase.execute(order_id=999)
            
    def test_sorting_orders_by_status_priority(self, customer_user):
        order1 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order1.created_at = datetime(2025, 2, 10, 10, 31, 15)
        order1.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PREPARING.status)
        self.order_gateway.update(order1)

        order2 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order2.created_at = datetime(2025, 2, 10, 10, 15, 20)
        order2.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        self.order_gateway.update(order2)

        order3 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order3.created_at = datetime(2025, 2, 10, 10, 5, 30)
        order3.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_READY.status)
        self.order_gateway.update(order3)

        order4 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order4.created_at = datetime(2025, 2, 10, 9, 25, 40)
        order4.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        self.order_gateway.update(order4)

        order5 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order5.created_at = datetime(2025, 2, 10, 9, 15, 50)
        order5.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_READY.status)
        self.order_gateway.update(order5)
    
        orders = self.list_orders_usecase.execute()

        assert orders[0].id == order4.id # created_at: 9:25:40, status: ORDER_PAID
        assert orders[1].id == order2.id # created_at: 10:15:20, status: ORDER_PAID
        assert orders[2].id == order1.id # created_at: 10:31:15, status: ORDER_PREPARING
        assert orders[3].id == order5.id # created_at: 9:15:50, status: ORDER_READY
        assert orders[4].id == order3.id # created_at: 10:05:30, status: ORDER_READY

    def test_list_orders_with_default_status_filter(self, customer_user):
        order1 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order1.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        self.order_gateway.update(order1)

        order2 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order2.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PREPARING.status)
        self.order_gateway.update(order2)

        order3 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order3.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_READY.status)
        self.order_gateway.update(order3)

        order4 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order4.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_COMPLETED.status)
        self.order_gateway.update(order4)

        order5 = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])
        order5.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PLACED.status)
        
        orders = self.list_orders_usecase.execute()
        
        assert len(orders) == 3
        assert orders[0].id == order1.id
        assert orders[1].id == order2.id
        assert orders[2].id == order3.id

    def test_get_order_status_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer_id=customer_user['person']['id'])

        status = self.get_order_status_usecase.execute(order.id, current_user=customer_user)

        assert status == order.order_status

