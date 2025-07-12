from typing import TYPE_CHECKING, Optional
from src.core.domain.entities.base_entity import BaseEntity

if TYPE_CHECKING:
    from src.core.domain.entities.order import Order
    from src.core.domain.entities.product import Product

class OrderItem(BaseEntity):
    
    def __init__(
        self,
        order: Optional['Order'] = None,
        product: Optional['Product'] = None,
        quantity: Optional[int] = 1,
        observation: Optional[str] = "",
        id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        inactivated_at: Optional[str] = None
    ):
        super().__init__(id, created_at, updated_at, inactivated_at)
        self.order = order
        self.product = product
        self.quantity = quantity
        self.observation = observation

    @property
    def order(self) -> 'Order':
        return self._order

    @order.setter
    def order(self, value: 'Order'):
        self._order = value

    @property
    def product(self) -> 'Product':
        return self._product

    @product.setter
    def product(self, value: 'Product'):
        self._product = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        self._quantity = value

    @property
    def observation(self) -> Optional[str]:
        return self._observation

    @observation.setter
    def observation(self, value: Optional[str]):
        self._observation = value.strip() if value else value
    

    @property
    def total(self) -> float:
        """
        Calculates the total cost of this item based on the product price and quantity.

        :return: Total cost as a float.
        """
        return self.product.price * self.quantity
    
    @property
    def product_category(self):
        """
        Retrieves the category of the associated product.

        :return: The category of the product.
        """
        return self.product.category
