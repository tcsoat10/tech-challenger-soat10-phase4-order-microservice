# import pytest

# from src.adapters.driven.repositories.order_payment_repository import OrderPaymentRepository
# from src.core.domain.entities.order_payment import OrderPayment
# from tests.factories.order_factory import OrderFactory
# from tests.factories.payment_factory import PaymentFactory
# from tests.factories.order_payment_factory import OrderPaymentFactory


# class TestOrderPaymentRepository:
#     @pytest.fixture(autouse=True)
#     def setup(self, db_session):
#         self.repository = OrderPaymentRepository(db_session)
#         self.db_session = db_session
#         self.clean_database()

#     def clean_database(self):
#         self.db_session.query(OrderPayment).delete()
#         self.db_session.commit()

#     def test_create_order_payment_success(self):
#         order = OrderFactory()
#         payment = PaymentFactory()

#         order_payment = OrderPayment(order_id=order.id, payment_id=payment.id)

#         created_order = self.repository.create(order_payment)

#         assert created_order.id is not None
#         assert created_order.order_id == order.id
#         assert created_order.payment_id == payment.id

#     def test_get_order_payment_by_id_return_success(self):
#         order_payment = OrderPaymentFactory()

#         order_payment_response = self.repository.get_by_id(order_payment.id)

#         assert order_payment_response is not None
#         assert order_payment_response.id == order_payment.id
#         assert order_payment_response.order_id == order_payment.order_id
#         assert order_payment_response.payment_id == order_payment.payment_id
    
#     def test_get_order_payment_by_order_id_return_success(self):
#         order_payment = OrderPaymentFactory()

#         order_payment_response = self.repository.get_by_order_id(order_payment.order_id)

#         assert order_payment_response is not None
#         assert order_payment_response.id == order_payment.id
#         assert order_payment_response.order_id == order_payment.order_id
#         assert order_payment_response.payment_id == order_payment.payment_id

#     def test_get_order_payment_by_payment_id_return_success(self):
#         order_payment = OrderPaymentFactory()

#         order_payment_response = self.repository.get_by_payment_id(order_payment.payment_id)

#         assert order_payment_response is not None
#         assert order_payment_response.id == order_payment.id
#         assert order_payment_response.order_id == order_payment.order_id
#         assert order_payment_response.payment_id == order_payment.payment_id

#     def test_get_order_payment_by_id_return_none_for_unregistered_id(self):
#         order_payment = OrderPaymentFactory()

#         order_payment_response = self.repository.get_by_id(order_payment.id + 1)

#         assert order_payment_response is None

#     def test_get_order_payment_by_order_id_return_none_for_unregistered_id(self):
#         order_payment = OrderPaymentFactory()

#         order_payment_response = self.repository.get_by_order_id(order_payment.order_id + 1)

#         assert order_payment_response is None

#     def test_get_order_payment_by_payment_id_return_none_for_unregistered_id(self):
#         order_payment = OrderPaymentFactory()

#         order_payment_response = self.repository.get_by_payment_id(order_payment.order_id + 1)

#         assert order_payment_response is None

#     def test_get_all_order_payments_return_sucess(self):
#         order_payment1 = OrderPaymentFactory()
#         order_payment2 = OrderPaymentFactory()

#         order_payments = self.repository.get_all()

#         assert len(order_payments) == 2
#         assert order_payments == [order_payment1, order_payment2]

#     def test_get_all_order_payments_empty_db(self):
#         order_payments = self.repository.get_all()

#         assert len(order_payments) == 0
#         assert order_payments == []

#     def test_update_order_payment_success(self):
#         order_payment = OrderPaymentFactory()
#         order = OrderFactory()
#         payment = PaymentFactory()

#         order_payment.order_id = order.id
#         order_payment.payment_id = payment.id

#         data = self.repository.update(order_payment)

#         assert data.id == order_payment.id
#         assert data.order_id == order.id
#         assert data.payment_id == payment.id

#     def test_delete_order_payment_success(self):
#         order_payment = OrderPaymentFactory()

#         self.repository.delete(order_payment.id)

#         data = self.repository.get_all()

#         assert len(data) == 0
#         assert data == []

#     def test_delete_order_payment_unregistered_id(self):
#         order_payment = OrderPaymentFactory()

#         self.repository.delete(order_payment.id + 1)

#         data = self.repository.get_all()

#         assert len(data) == 1
#         assert data == [order_payment]