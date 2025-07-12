import pytest
from sqlalchemy.exc import IntegrityError

from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.core.domain.entities.order_status import OrderStatus
from tests.factories.order_status_factory import OrderStatusFactory
from src.adapters.driven.repositories.models.order_status_model import OrderStatusModel


class TestOrderStatusRepository:
    
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = OrderStatusRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(OrderStatusModel).delete()
        self.db_session.commit()

    def test_create_order_status_success(self):
        order_status = OrderStatus(status="PENDING", description="Order is pending")
        created_order_status = self.repository.create(order_status)

        assert created_order_status.id is not None
        assert created_order_status.status == "PENDING"
        assert created_order_status.description == "Order is pending"

        db_order_status = self.db_session.query(OrderStatusModel).filter_by(status="PENDING").first()
        assert db_order_status is not None
        assert db_order_status.status == "PENDING"
        assert db_order_status.description == "Order is pending"

    def test_exists_by_status_success(self):
        OrderStatusFactory(status="PENDING", description="Order is pending")

        assert self.repository.exists_by_status("PENDING") is True

    def test_exists_by_status_failure(self):
        assert self.repository.exists_by_status("PENDING") is False

    def test_try_create_order_status_duplicated_with_repository_and_raise_error(self):
        OrderStatusFactory(status="PENDING", description="Order is pending")

        order_status = OrderStatus(status="PENDING", description="Order is pending")
        with pytest.raises(IntegrityError):
            self.repository.create(order_status)

    def test_get_by_status_success(self):
        OrderStatusFactory(status="PENDING", description="Order is pending")

        order_status_from_db = self.repository.get_by_status("PENDING")

        assert order_status_from_db is not None
        assert order_status_from_db.status == "PENDING"
        assert order_status_from_db.description == "Order is pending"

    def test_get_by_id_success(self):
        order_status = OrderStatusFactory(status="PENDING", description="Order is pending")

        order_status_from_db = self.repository.get_by_id(order_status.id)

        assert order_status_from_db is not None
        assert order_status_from_db.status == "PENDING"
        assert order_status_from_db.description == "Order is pending"

    def test_get_all_success(self):
        OrderStatusFactory(status="PENDING", description="Order is pending")
        OrderStatusFactory(status="CONFIRMED", description="Order is confirmed")

        order_statuses_from_db = self.repository.get_all()

        assert len(order_statuses_from_db) == 2
        assert order_statuses_from_db[0].status == "PENDING"
        assert order_statuses_from_db[0].description == "Order is pending"
        assert order_statuses_from_db[1].status == "CONFIRMED"
        assert order_statuses_from_db[1].description == "Order is confirmed"
    
    def test_update_order_status_success(self):
        order_status: OrderStatus = OrderStatusFactory(status="PENDING", description="Order is pending")

        order_status.status = "CONFIRMED"
        order_status.description = "Order is confirmed"
        updated_order_status = self.repository.update(order_status)

        assert updated_order_status.id is not None
        assert updated_order_status.status == "CONFIRMED"
        assert updated_order_status.description == "Order is confirmed"

        db_order_status = self.db_session.query(OrderStatusModel).filter_by(status="CONFIRMED").first()
        assert db_order_status is not None
        assert db_order_status.status == "CONFIRMED"
        assert db_order_status.description == "Order is confirmed"

    def test_delete_order_status_success(self): 
        order_status = OrderStatusFactory(status="PENDING", description="Order is pending")

        self.repository.delete(order_status)

        db_order_status = self.db_session.query(OrderStatusModel).filter_by(status="PENDING").first()
        assert db_order_status is None
