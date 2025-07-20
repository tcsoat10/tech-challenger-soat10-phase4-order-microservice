import uuid
import pytest
from sqlalchemy.exc import IntegrityError
from src.adapters.driven.repositories.models.order_item_model import OrderItemModel
from src.core.domain.entities.order_item import OrderItem
from src.adapters.driven.repositories.order_item_repository import OrderItemRepository
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory


class TestOrderItemRepository:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = OrderItemRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(OrderItemModel).delete()
        self.db_session.commit()

    def test_create_order_item_success(self):
        order = OrderFactory()
        order_item = OrderItem(
            order=order,
            product_name="Burger",
            product_sku="burger-001",
            product_id=str(uuid.uuid4()),
            product_price=6.0,
            product_category_name="Fast Food",
            quantity=2,
            observation="No onions"
        )
        created_order_item = self.repository.create(order_item)

        assert created_order_item.id is not None
        assert created_order_item.product_id == order_item.product_id
        assert created_order_item.product_name == "Burger"
        assert created_order_item.product_sku == "burger-001"
        assert created_order_item.total == 12.0
        assert created_order_item.quantity == 2

        db_order_item = self.repository.get_by_id(created_order_item.id)
        assert db_order_item is not None
        assert db_order_item.product_id == order_item.product_id
        assert db_order_item.total == 12.0
        assert db_order_item.product_category == 'Fast Food'

    def test_try_create_order_item_duplicated_with_repository_and_raise_error(self, db_session):
        OrderItemFactory(
            product_name="Burger",
            product_sku="burger-001",
            product_id=str(uuid.uuid4()),
            product_price=6.0,
            product_category_name="Fast Food",
            quantity=2,
            observation="No onions"
        )

        new = OrderItem(
            product_name="Burger",
            product_sku="burger-001",
            product_id=str(uuid.uuid4()),
            product_price=6.0,
            product_category_name="Fast Food",
            quantity=2,
            observation="No onions"
        )
        with pytest.raises(IntegrityError):
            self.repository.create(new)

    def test_get_by_product_name_success(self):
        '''order_item = OrderItemFactory(
            product_name="Burger",
            product_sku="burger-001",
            product_id=uuid.uuid4(),
            product_price=6.0,
            product_category_name="Fast Food",
            quantity=2,
            observation="No onions"
        )'''
        order_item = OrderItemFactory()

        order_items_from_db = self.repository.get_by_product_name(order_item.order_id, order_item.product_name)

        assert order_items_from_db.product_id == order_item.product_id
        assert order_items_from_db.quantity == order_item.quantity
        assert order_items_from_db.observation == order_item.observation
        assert order_items_from_db.total == order_item.quantity * order_item.product_price

    def test_get_by_product_name_with_no_product_registered(self):
        OrderItemFactory(
            product_name="MilkShake",
            product_price=9.0,
            product_sku="milkshake-001",
            product_id=str(uuid.uuid4()),
            product_category_name="Beverage",
            quantity=2,
            observation="No onions"
        )

        order_items_from_db = self.repository.get_by_product_name(1, "Burger")

        assert order_items_from_db is None

    def test_get_by_order_id_success(self):
        order_item = OrderItemFactory(quantity=2, observation="No onions")

        order_items_from_db = self.repository.get_by_order_id(order_item.order_id)

        assert len(order_items_from_db) == 1
        assert order_items_from_db[0].product_id == order_item.product_id
        assert order_items_from_db[0].quantity == 2
        assert order_items_from_db[0].observation == "No onions"
        assert order_items_from_db[0].total == order_item.quantity * order_item.product_price

    def test_get_order_item_by_id_success(self):
        order_item = OrderItemFactory(quantity=2, observation="No onions")

        order_item_from_db = self.repository.get_by_id(order_item.id)

        assert order_item_from_db is not None
        assert order_item_from_db.product_id == order_item.product_id
        assert order_item_from_db.quantity == 2
        assert order_item_from_db.observation == "No onions"
        assert order_item_from_db.total == order_item.quantity * order_item.product_price

    def test_get_order_item_by_id_with_no_id_registered(self):
        OrderItemFactory(id=1)

        order_item_from_db = self.repository.get_by_id(2)

        assert order_item_from_db is None

    def test_get_all_order_items(self):
        order_item1 = OrderItemFactory(product_name="Burger", product_price=15.0, quantity=2, observation="No onions")
        order_item2 = OrderItemFactory(product_name="MilkShake", product_price=9.0, quantity=1, observation="")

        order_items = self.repository.get_all()

        assert len(order_items) == 2
        assert order_items[0].product_id == order_item1.product_id
        assert order_items[0].quantity == 2
        assert order_items[0].observation == "No onions"
        assert order_items[0].total == 30.0

        assert order_items[1].product_id == order_item2.product_id
        assert order_items[1].observation == ""
        assert order_items[1].quantity == 1
        assert order_items[1].total == 9.0

    def test_get_all_order_items_with_empty_db(self):
        order_items = self.repository.get_all()

        assert len(order_items) == 0
        assert order_items == []

    def test_update_order_item(self):
        order_item = OrderItemFactory(product_name="Burger", product_price=15.0, quantity=2, observation="No onions")
        order_item.observation = "No pickles"
        order_item.quantity = 3

        updated_order_item = self.repository.update(order_item)

        assert updated_order_item.observation == "No pickles"
        assert updated_order_item.quantity == 3
        assert updated_order_item.total == 45.0

    def test_delete_order_item(self):
        order_item = OrderItemFactory()
        self.repository.delete(order_item)

        assert len(self.repository.get_all()) == 0
