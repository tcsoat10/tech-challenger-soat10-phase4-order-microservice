import factory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyInteger
from faker import Faker

from src.adapters.driven.repositories.models.order_item_model import OrderItemModel

fake = Faker()

class OrderItemFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OrderItemModel
        sqlalchemy_session_persistence = "commit"


    order = factory.SubFactory("tests.factories.order_factory.OrderFactory")
    order_id = factory.LazyAttribute(lambda obj: obj.order.id)

    product_name = factory.LazyAttribute(lambda _: fake.word())
    product_sku = factory.LazyAttribute(lambda _: fake.word())
    product_id = factory.LazyAttribute(lambda _: fake.uuid4())
    product_name = factory.LazyAttribute(lambda _: fake.word())
    product_category_name = factory.LazyAttribute(lambda _: fake.word())

    quantity = FuzzyInteger(1, 10)
    observation = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
