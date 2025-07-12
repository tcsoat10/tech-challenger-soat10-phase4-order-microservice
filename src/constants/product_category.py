from enum import Enum


class ProductCategoryEnum(Enum):
    BURGERS = ("burgers", "meat, chicken and fish burgers")
    SIDES = ("side dishes", "fries, onions, chicken nuggets")
    DRINKS = ("drinks", "soda, juice, water and beers")
    DESSERTS = ("desserts", "ice cream and smoothies")

    @property
    def name(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    @classmethod
    def values_and_descriptions(cls):
        return [{"name": member.name, "description": member.description} for member in cls]
