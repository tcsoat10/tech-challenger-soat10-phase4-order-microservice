from datetime import datetime
import pytest
from pycpfcnpj import gen
from unittest.mock import patch

from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from src.constants.product_category import ProductCategoryEnum

from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.entities.order_item import OrderItem

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
    def mock_stock_gateway(self):
        def fake_get_category_by_name(category_name):
            if category_name == "burgers":
                return {
                "id": 1,
                "name": ProductCategoryEnum.BURGERS.name,
                "description": ProductCategoryEnum.BURGERS.description
                }
            if category_name == "sides":
                return {
                "id": 2,
                "name": ProductCategoryEnum.SIDES.name,
                "description": ProductCategoryEnum.SIDES.description
                }
            if category_name == "drinks":
                return {
                "id": 3,
                "name": ProductCategoryEnum.DRINKS.name,
                "description": ProductCategoryEnum.DRINKS.description
                }
            if category_name == "desserts":
                return {
                "id": 4,
                "name": ProductCategoryEnum.DESSERTS.name,
                "description": ProductCategoryEnum.DESSERTS.description
                }
            # Simule produto não encontrado
            return None
        
        def fake_get_products_by_category_id(category_id):
            # Retorne uma lista fake de produtos conforme esperado pelo seu código
            if category_id == 1:
                return [OrderItem(
                id=1,
                product_name="Burger",
                product_sku="burger-001",
                product_id=1,
                product_price=6.0,
                product_category_name="burgers",
                quantity=2,
                observation="No onions"
                )]
            if category_id == 2:
                return [OrderItem(
                id=2,
                product_name="Fries",
                product_sku="fries-001",
                product_id=2,
                product_price=3.0,
                product_category_name="sides",
                quantity=1,
                observation=""
                )]
            if category_id == 3:
                return [OrderItem(
                id=3,
                product_name="Soda",
                product_sku="soda-001",
                product_id=3,
                product_price=2.0,
                product_category_name="drinks",
                quantity=1,
                observation=""
                )]
            if category_id == 4:
                return [OrderItem(
                id=4,
                product_name="Ice Cream",
                product_sku="icecream-001",
                product_id=4,
                product_price=4.0,
                product_category_name="desserts",
                quantity=1,
                observation=""
                )]        
            return []
        def fake_get_product_by_id(product_id):
            # Retorne um produto fake conforme esperado pelo seu código
            if product_id == 1:
                return OrderItem(
                    id=1,
                    product_name="Burger",
                    product_sku="burger-001",
                    product_id=1,
                    product_price=6.0,
                    product_category_name=ProductCategoryEnum.BURGERS.name,
                    quantity=2,
                    observation="No onions"
                )
            return None        

        with patch.object(
            StockMicroserviceGateway,
            "get_category_by_name",
            side_effect=fake_get_category_by_name
        ), patch.object(
            StockMicroserviceGateway,
            "get_products_by_category_id",
            side_effect=fake_get_products_by_category_id
        ), patch.object(
            StockMicroserviceGateway,
            "get_product_by_id",
            side_effect=fake_get_product_by_id
        ):
            yield
    
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
        return 'customer'
        '''return {
            "profile": {"name": "customer"},
            "person": {"id": str(self.test_customer.person.id)}
        }'''
    
    def test_create_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        assert order.id is not None
        assert order.id_customer == customer_user
        assert order.order_status.status == OrderStatusEnum.ORDER_PENDING.status
    '''
    def test_create_order_when_open_order_exists(self, customer_user):
        self.create_order_usecase.execute(customer=customer_user)
        
        with pytest.raises(BadRequestException, match="Já existe um pedido em aberto para este cliente"):
            self.create_order_usecase.execute(customer=customer_user)
    '''

    def test_list_orders_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        order.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        self.order_gateway.update(order)
        
        orders = self.list_orders_usecase.execute()
        
        assert len(orders) == 1
        assert orders[0].id == order.id
    
    def test_advance_order_status_to_waiting_burgers(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        updated_order = self.advance_order_status_usecase.execute(order_id=order.id)
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
    
    def test_add_order_item_in_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        self.advance_order_status_usecase.execute(order_id=order.id)
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=2,
            observation="No pickles"
        )
        
        updated_order = self.add_order_item_usecase.execute(
            order_id=order.id,
            order_item_dto=order_item_dto
        )
        
        assert len(updated_order.order_items) == 1
        assert updated_order.order_items[0].product_id == self.burger_order_item['product_id']
        assert updated_order.order_items[0].quantity == 2
        assert updated_order.order_items[0].observation == "No pickles"
    
    def test_list_order_items_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        self.advance_order_status_usecase.execute(order_id=order.id)
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=2,
            observation="No pickles"
        )
        
        self.add_order_item_usecase.execute(order_id=order.id, order_item_dto=order_item_dto)
        
        order_items = self.list_order_items_usecase.execute(order_id=order.id)
        
        assert len(order_items) == 1
        assert order_items[0].product_id == self.burger_order_item['product_id']
        assert order_items[0].quantity == 2
    
    def test_change_item_quantity_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        self.advance_order_status_usecase.execute(order_id=order.id)
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=2,
            observation="No pickles"
        )
        
        updated_order = self.add_order_item_usecase.execute(order_id=order.id, order_item_dto=order_item_dto)
        
        order_item_id = updated_order.order_items[0].id
        
        self.change_item_quantity_usecase.execute(order_id=order.id, order_item_id=order_item_id, new_quantity=3)
        
        order_items = self.list_order_items_usecase.execute(order_id=order.id)
        
        assert order_items[0].quantity == 3
    
    def test_remove_order_item_from_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        self.advance_order_status_usecase.execute(order_id=order.id)
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=1,
            observation="No pickles"
        )
        
        updated_order = self.add_order_item_usecase.execute(order_id=order.id, order_item_dto=order_item_dto)
        
        order_item_id = updated_order.order_items[0].id
        
        self.remove_order_item_usecase.execute(order_id=order.id, order_item_id=order_item_id)
        
        order_items = self.list_order_items_usecase.execute(order_id=order.id)
        
        assert len(order_items) == 0
    
    def test_clear_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        self.advance_order_status_usecase.execute(order_id=order.id)
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_order_item['product_id'],
            quantity=2,
            observation="No pickles"
        )
        
        self.add_order_item_usecase.execute(order_id=order.id, order_item_dto=order_item_dto)        
        
        self.clear_order_usecase.execute(order_id=order.id)
        
        order_items = self.list_order_items_usecase.execute(order_id=order.id)
        
        assert len(order_items) == 0
    
    def test_revert_order_status_usecase_when_order_is_waiting_burgers_and_return_error(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        updated_order = self.advance_order_status_usecase.execute(order_id=order.id)
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
        
        with pytest.raises(BadRequestException) as exc:
            self.revert_order_status_usecase.execute(order_id=order.id)
        
        assert exc.value.args[0] == "O status atual 'order_waiting_burgers' não permite voltar."
        
    def test_revert_order_status_usecase_when_order_is_waiting_side_dishes_and_return_success(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        updated_order = self.advance_order_status_usecase.execute(order_id=order.id)
        updated_order = self.advance_order_status_usecase.execute(order_id=order.id)
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_SIDES.status

        self.revert_order_status_usecase.execute(order_id=order.id)
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
    
    def test_list_products_by_order_status_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)
        
        self.advance_order_status_usecase.execute(order_id=order.id)
        
        products = self.list_products_by_order_status_usecase.execute(order_id=order.id)
        
        assert len(products) == 1
        assert products[0].id == self.burger_order_item['product_id']
    
    def test_access_non_existent_order(self, customer_user):
        with pytest.raises(EntityNotFoundException):
            self.list_order_items_usecase.execute(order_id=999)
            
    def test_sorting_orders_by_status_priority(self, customer_user):
        order1 = self.create_order_usecase.execute(customer=customer_user)
        order1.created_at = datetime(2025, 2, 10, 10, 31, 15)
        order1.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PREPARING.status)
        self.order_gateway.update(order1)
        
        order2 = self.create_order_usecase.execute(customer=customer_user)
        order2.created_at = datetime(2025, 2, 10, 10, 15, 20)
        order2.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        self.order_gateway.update(order2)
        
        order3 = self.create_order_usecase.execute(customer=customer_user)
        order3.created_at = datetime(2025, 2, 10, 10, 5, 30)
        order3.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_READY.status)
        self.order_gateway.update(order3)
        
        order4 = self.create_order_usecase.execute(customer=customer_user)
        order4.created_at = datetime(2025, 2, 10, 9, 25, 40)
        order4.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        self.order_gateway.update(order4)
        
        order5 = self.create_order_usecase.execute(customer=customer_user)
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
        order1 = self.create_order_usecase.execute(customer=customer_user)
        order1.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        self.order_gateway.update(order1)
        
        order2 = self.create_order_usecase.execute(customer=customer_user)
        order2.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PREPARING.status)
        self.order_gateway.update(order2)
        
        order3 = self.create_order_usecase.execute(customer=customer_user)
        order3.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_READY.status)
        self.order_gateway.update(order3)
        
        order4 = self.create_order_usecase.execute(customer=customer_user)
        order4.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_COMPLETED.status)
        self.order_gateway.update(order4)
        
        order5 = self.create_order_usecase.execute(customer=customer_user)
        order5.order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PLACED.status)
        
        orders = self.list_orders_usecase.execute()
        
        assert len(orders) == 3
        assert orders[0].id == order1.id
        assert orders[1].id == order2.id
        assert orders[2].id == order3.id

    def test_get_order_status_usecase(self, customer_user):
        order = self.create_order_usecase.execute(customer=customer_user)

        status = self.get_order_status_usecase.execute(order.id)

        assert status == order.order_status

