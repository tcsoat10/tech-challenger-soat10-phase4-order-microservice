import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.adapters.driven.repositories.models.order_status_model import OrderStatusModel


fake = Faker()


class OrderStatusFactory(SQLAlchemyModelFactory):
    
    class Meta:
        model = OrderStatusModel
        sqlalchemy_session_persistence = "commit"

    status = factory.LazyAttribute(lambda _: fake.sentence(nb_words=2))
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
    