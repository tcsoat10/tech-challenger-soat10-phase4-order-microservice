import pytest
from sqlalchemy.exc import IntegrityError

from src.adapters.driven.repositories.models.order_model import OrderModel
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.constants.product_category import ProductCategoryEnum
from src.core.exceptions.bad_request_exception import BadRequestException
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.core.domain.entities.order import Order
from src.constants.order_status import OrderStatusEnum
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from tests.factories.order_status_factory import OrderStatusFactory


class TestOrderRepository:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = OrderRepository(db_session)
        self.order_status_repository = OrderStatusRepository(db_session)
        self.db_session = db_session
        self._populate_status_order()
        self.clean_database()

    def _populate_status_order(self):
        OrderStatusFactory(status=OrderStatusEnum.ORDER_PENDING.status, description=OrderStatusEnum.ORDER_PENDING.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_SIDES.status, description=OrderStatusEnum.ORDER_WAITING_SIDES.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_DRINKS.status, description=OrderStatusEnum.ORDER_WAITING_DRINKS.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_DESSERTS.status, description=OrderStatusEnum.ORDER_WAITING_DESSERTS.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_READY_TO_PLACE.status, description=OrderStatusEnum.ORDER_READY_TO_PLACE.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_PLACED.status, description=OrderStatusEnum.ORDER_PLACED.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_PAID.status, description=OrderStatusEnum.ORDER_PAID.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_PREPARING.status, description=OrderStatusEnum.ORDER_PREPARING.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_READY.status, description=OrderStatusEnum.ORDER_READY.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_COMPLETED.status, description=OrderStatusEnum.ORDER_COMPLETED.description)
        OrderStatusFactory(status=OrderStatusEnum.ORDER_CANCELLED.status, description=OrderStatusEnum.ORDER_CANCELLED.description)

    def clean_database(self):
        self.db_session.query(OrderModel).delete()
        self.db_session.commit()

    def test_create_order_success(self):
        customer = 'customer'
        order_status = self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_PENDING.status)
        employee = 'employee'
        order = Order(id_customer=customer, order_status=order_status, id_employee=employee)
        created_order = self.repository.create(order)

        assert created_order.id is not None
        assert created_order.id_customer == customer
        assert created_order.order_status.id == order_status.id
        assert created_order.id_employee == employee

    def test_try_create_order_duplicated_with_repository_and_raise_error(self):
        
        #order_status = self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_PENDING.status)
        #order = Order(customer=customer, order_status=order_status)
        order = OrderFactory()
        with pytest.raises(IntegrityError):
            self.repository.create(order)

    def test_get_order_by_customer_id_success(self):
        order = OrderFactory()

        order_from_db = self.repository.get_by_customer_id(order.id_customer)
        assert order_from_db is not None
    
    def test_get_order_by_employee_id_success(self):
        order = OrderFactory()

        order_from_db = self.repository.get_by_customer_id(order.id_employee)
        assert order_from_db is not None

    def test_get_by_id_success(self):
        order = OrderFactory()

        order_from_db = self.repository.get_by_id(order.id)

        assert order_from_db is not None
        assert order_from_db.id_customer == order.id_customer
        assert order_from_db.order_status.id == order.order_status.id
        assert order_from_db.id_employee == order.id_employee        

    def test_get_all_success(self):
        '''
        person1 = PersonFactory(cpf="12345678901", name="JOÃO", email="joao@gmail.com")
        customer = CustomerFactory(person=person1)
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        OrderFactory(customer=customer, order_status=order_status, employee=employee)
        
        person2 = PersonFactory(cpf="12345678902", name="PAULO", email="paulo@outlook.com")
        customer = CustomerFactory(person=person2)
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        OrderFactory(customer=customer, order_status=order_status, employee=employee)
        '''
        order1 = OrderFactory()
        order2 = OrderFactory()

        orders_from_db = self.repository.get_all()

        assert len(orders_from_db) == 2
        assert orders_from_db[0].id_customer == order1.id_customer
        assert orders_from_db[1].id_customer == order2.id_customer
        assert orders_from_db[0].order_status.id == order1.order_status.id
        assert orders_from_db[1].order_status.id == order2.order_status.id
        assert orders_from_db[0].id_employee == order1.id_employee
        assert orders_from_db[1].id_employee == order2.id_employee        

    def test_update_order_success(self):
        order = OrderFactory()

        #Dá para atualizar direto no campo passando o caminho correto.
        order.id_customer = "teste"
        # order.id_customer = customer2.id
        updated_order = self.repository.update(order)

        assert updated_order.id is not None
        assert updated_order.id_customer == "teste"
        assert updated_order.id == order.id
        assert updated_order.order_status.id == order.order_status.id
        assert updated_order.id_employee == order.id_employee

    def test_delete_order_success(self):
        order = OrderFactory()

        self.repository.delete(order)
        
        db_order = self.repository.get_by_id(order.id)
        assert db_order is None

    #@patch('src.core.domain.entities.order.Order.is_paid', new_callable=PropertyMock)
    def test_order_next_step_success(self):
        #mock_is_paid.return_value = True

        #person = PersonFactory()
        #customer = CustomerFactory(person=person)
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_PENDING.status),
            id_employee='employee'
        )
        
        
        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_PENDING.status
        assert order.status_history[-1].changed_by == 'System'

        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status

        order_model = self.db_session.query(OrderModel).filter(OrderModel.id == order.id).first()
        order_item1 = OrderItemFactory(
            order=order_model,
            product_category_name=ProductCategoryEnum.BURGERS.name,
        )
        order.add_item(order_item1.to_entity())
        order.advance_order_status(self.order_status_repository)
        
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_SIDES.status
        
        order_item2 = OrderItemFactory(
            order=order_model,
            product_category_name=ProductCategoryEnum.SIDES.name,
        )
        order.add_item(order_item2.to_entity())
        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_DRINKS.status
        
        order_item3 = OrderItemFactory(
            order=order_model,
            product_category_name=ProductCategoryEnum.DRINKS.name
        )
        order.add_item(order_item3.to_entity())
        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_DESSERTS.status

        order_item4 = OrderItemFactory(
            order=order_model,
            product_category_name=ProductCategoryEnum.DESSERTS.name
        )
        order.add_item(order_item4.to_entity())
        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_READY_TO_PLACE.status

        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_PLACED.status
        assert order.status_history[-1].changed_by == order.id_customer

        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_PAID.status
        assert order.status_history[-1].changed_by == 'System'

        employee = 'employee'
        order.advance_order_status(self.order_status_repository, employee=employee)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_PREPARING.status
        assert order.status_history[-1].changed_by == order.id_employee

        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_READY.status
        assert order.status_history[-1].changed_by == order.id_employee

        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_COMPLETED.status
        assert order.status_history[-1].changed_by == order.id_employee

    
    def test_cancel_order_cancel_when_status_is_order_pending(self):        
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_PENDING.status),
            id_employee='employee'
        )
        
        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_PENDING.status
        assert order.status_history[-1].changed_by == 'System'

        order.cancel_order(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_CANCELLED.status
        assert order.status_history[-1].changed_by == order.id_customer

        with pytest.raises(BadRequestException) as exc:
            order.advance_order_status(self.order_status_repository)

        assert exc.value.detail['message'] == "O estado atual order_cancelled não permite transições."
    
    def test_cancel_order_cancel_when_status_is_order_placed(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_PLACED.status),
            id_employee='employee'
        )
        
        order = self.repository.create(order)

        assert order.order_status.status == OrderStatusEnum.ORDER_PLACED.status
        order.cancel_order(self.order_status_repository)
        order = self.repository.update(order)

        assert order.order_status.status == OrderStatusEnum.ORDER_CANCELLED.status
        assert order.status_history[-1].changed_by == order.id_customer

        with pytest.raises(BadRequestException) as exc:
            order.advance_order_status(self.order_status_repository)

        assert exc.value.detail['message'] == "O estado atual order_cancelled não permite transições."
    
    def test_cancel_order_cancel_when_status_is_order_paid(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_PAID.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        with pytest.raises(BadRequestException) as exc:
            order.cancel_order(self.order_status_repository)

        assert exc.value.detail['message'] == "O pedido não está em um estado válido para cancelar o pedido."

    def test_go_back_order_when_status_is_order_ready_to_place(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_READY_TO_PLACE.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_READY_TO_PLACE.status
        
        order.revert_order_status(self.order_status_repository)
        order = self.repository.update(order)

        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_DESSERTS.status

    def test_go_back_order_when_status_is_order_placed(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_PLACED.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_PLACED.status

        with pytest.raises(BadRequestException) as exc:
            order.revert_order_status(self.order_status_repository)
        
        assert exc.value.detail['message'] == "O status atual 'order_placed' não permite voltar."

    def test_go_back_order_when_status_is_order_waiting_burgers(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_BURGERS.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status

        with pytest.raises(BadRequestException) as exc:
            order.revert_order_status(self.order_status_repository)
        
        assert exc.value.detail['message'] == "O status atual 'order_waiting_burgers' não permite voltar."

    def test_go_back_order_when_status_is_order_waiting_sides(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_SIDES.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_SIDES.status

        order.revert_order_status(self.order_status_repository)
        order = self.repository.update(order)

        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status

    def test_go_back_order_when_status_is_order_waiting_drinks(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_DRINKS.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_DRINKS.status

        order.revert_order_status(self.order_status_repository)
        order = self.repository.update(order)

        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_SIDES.status
    
    def test_go_back_order_when_status_is_order_waiting_desserts(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_DESSERTS.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_DESSERTS.status

        order.revert_order_status(self.order_status_repository)
        order = self.repository.update(order)

        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_DRINKS.status

    def test_order_send_item_with_the_incorrect_category(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_BURGERS.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status

        with pytest.raises(BadRequestException) as exc:
            order_model = self.db_session.query(OrderModel).filter(OrderModel.id == order.id).first()
            order_item = OrderItemFactory(
                order=order_model,
                product_category_name=ProductCategoryEnum.SIDES.name
            )
            order.add_item(order_item.to_entity())
        
        assert exc.value.detail['message'] == "Não é possível adicionar itens da categoria 'side dishes' no status atual 'order_waiting_burgers'."

    def test_clear_order_items_success(self):
        order = Order(
            id_customer='customer',
            order_status=self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_BURGERS.status),
            id_employee='employee'
        )

        order = self.repository.create(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status

        order_model = self.db_session.query(OrderModel).filter(OrderModel.id == order.id).first()
        order_item1 = OrderItemFactory(
            order=order_model,
            product_category_name=ProductCategoryEnum.BURGERS.name
        )
        order.add_item(order_item1)
        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_SIDES.status

        order_item2 = OrderItemFactory(
            order=order_model,
            product_category_name=ProductCategoryEnum.SIDES.name
        )
        order.add_item(order_item2)
        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_DRINKS.status

        order_item3 = OrderItemFactory(
            order=order_model,
            product_category_name=ProductCategoryEnum.DRINKS.name
        )
        order.add_item(order_item3)
        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_DESSERTS.status

        order_item4 = OrderItemFactory(
            order=order_model,
            product_category_name=ProductCategoryEnum.DESSERTS.name
        )
        order.add_item(order_item4)
        order.advance_order_status(self.order_status_repository)
        order = self.repository.update(order)
        assert order.order_status.status == OrderStatusEnum.ORDER_READY_TO_PLACE.status

        order.clear_order(self.order_status_repository)

        order = self.repository.update(order)
        assert len(order.order_items) == 0
        assert order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
