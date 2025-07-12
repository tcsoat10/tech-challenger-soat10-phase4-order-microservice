import factory
from factory.alchemy import SQLAlchemyModelFactory
from factory.fuzzy import FuzzyFloat
from faker import Faker

from src.adapters.driven.repositories.models.product_model import ProductModel
from tests.factories.category_factory import CategoryFactory

fake = Faker()

class ProductFactory(SQLAlchemyModelFactory):

    class Meta:
        model = ProductModel
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=15))
    category = factory.SubFactory(CategoryFactory)
    category_id = factory.SelfAttribute("category.id")
    price = FuzzyFloat(10.0, 100.0, precision=2)
    sla_product = factory.LazyAttribute(lambda _: fake.word())
