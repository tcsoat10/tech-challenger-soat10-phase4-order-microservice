import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.adapters.driven.repositories.models.order_model import OrderModel
from tests.factories.order_item_factory import OrderItemFactory
from tests.factories.order_status_factory import OrderStatusFactory

fake = Faker()

class OrderFactory(SQLAlchemyModelFactory):
    
    class Meta:
        model = OrderModel
        sqlalchemy_session_persistence = "commit"

    order_status = factory.SubFactory(OrderStatusFactory)
    id_order_status = factory.SelfAttribute("order_status.id")
    
    id_customer = factory.LazyAttribute(lambda _: fake.uuid4())
    
    id_employee = factory.LazyAttribute(lambda _: fake.uuid4())
    
    order_items = factory.RelatedFactoryList(
        OrderItemFactory,
        factory_related_name="order",
        size=0
    )
