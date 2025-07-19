from fastapi import status
import pytest
from unittest.mock import patch
import uuid

from src.constants.product_category import ProductCategoryEnum
from src.constants.order_status import OrderStatusEnum
from tests.factories.order_factory import OrderFactory
from tests.factories.order_item_factory import OrderItemFactory
from tests.factories.order_status_factory import OrderStatusFactory
from src.adapters.driven.providers.stock_provider.stock_microservice_gateway import StockMicroserviceGateway
from src.core.domain.entities.order_item import OrderItem


@pytest.fixture(autouse=True)
def mock_stock_gateway():
    def fake_get_category_by_name(category_name):
        if category_name == "burgers":
            return {
            "id": 1,
            "name": ProductCategoryEnum.BURGERS.name,
            "description": ProductCategoryEnum.BURGERS.description
            }
        if category_name == "sides":
            return {
            "id": 2,
            "name": ProductCategoryEnum.SIDES.name,
            "description": ProductCategoryEnum.SIDES.description
            }
        if category_name == "drinks":
            return {
            "id": 3,
            "name": ProductCategoryEnum.DRINKS.name,
            "description": ProductCategoryEnum.DRINKS.description
            }
        if category_name == "desserts":
            return {
            "id": 4,
            "name": ProductCategoryEnum.DESSERTS.name,
            "description": ProductCategoryEnum.DESSERTS.description
            }
        # Simule produto não encontrado
        return None
    
    def fake_get_products_by_category_id(category_id):
        # Retorne uma lista fake de produtos conforme esperado pelo seu código
        if category_id == 1:
            return [OrderItem(
            id=1,
            product_name="Burger",
            product_sku="burger-001",
            product_id=str(uuid.uuid4()),
            product_price=6.0,
            product_category_name="burgers",
            quantity=2,
            observation="No onions"
            )]
        if category_id == 2:
            return [OrderItem(
            id=2,
            product_name="Fries",
            product_sku="fries-001",
            product_id=str(uuid.uuid4()),
            product_price=3.0,
            product_category_name="sides",
            quantity=1,
            observation=""
            )]
        if category_id == 3:
            return [OrderItem(
            id=3,
            product_name="Soda",
            product_sku="soda-001",
            product_id=str(uuid.uuid4()),
            product_price=2.0,
            product_category_name="drinks",
            quantity=1,
            observation=""
            )]
        if category_id == 4:
            return [OrderItem(
            id=4,
            product_name="Ice Cream",
            product_sku="icecream-001",
            product_id=str(uuid.uuid4()),
            product_price=4.0,
            product_category_name="desserts",
            quantity=1,
            observation=""
            )]        
        return []
    def fake_get_product_by_id(product_id):
        # Retorne um produto fake conforme esperado pelo seu código
        if product_id == 1:
            return OrderItem(
                id=1,
                product_name="Burger",
                product_sku="burger-001",
                product_id=str(uuid.uuid4()),
                product_price=6.0,
                product_category_name=ProductCategoryEnum.BURGERS.name,
                quantity=2,
                observation="No onions"
            )
        return None        

    with patch.object(
        StockMicroserviceGateway,
        "get_category_by_name",
        side_effect=fake_get_category_by_name
    ), patch.object(
        StockMicroserviceGateway,
        "get_products_by_category_id",
        side_effect=fake_get_products_by_category_id
    ), patch.object(
        StockMicroserviceGateway,
        "get_product_by_id",
        side_effect=fake_get_product_by_id
    ):
        yield


def test_create_order_success(client, populate_order_status):
    payload={'id_customer': 'customer'}

    response = client.post(
        "/api/v1/orders",
        #permissions=[OrderPermissions.CAN_CREATE_ORDER],
        #profile_name="customer",
        json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    
    assert "id" in data
    assert data['customer'] == 'customer'
    assert data["order_status"]["status"] == OrderStatusEnum.ORDER_PENDING.status
    assert data["order_status"]["description"] == OrderStatusEnum.ORDER_PENDING.description

    
def test_list_products_by_order_status_and_return_success(client):
    """ person = PersonFactory()
    customer = CustomerFactory(person=person)
    
    category1 = CategoryFactory(name=ProductCategoryEnum.BURGERS.name, description=ProductCategoryEnum.BURGERS.description)
    category2 = CategoryFactory(name=ProductCategoryEnum.DRINKS.name, description=ProductCategoryEnum.DRINKS.description)

    product1 = ProductFactory(category=category1)
    ProductFactory(category=category2) """

    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)

    order_item = OrderItemFactory(product_category_name=ProductCategoryEnum.BURGERS.name, product_name="Burger")
    order = OrderFactory(id_customer='customer', order_status=order_status)
    order.order_items=[order_item]

    response = client.get(
        f"/api/v1/orders/{order.id}/products",
    )

    assert response.status_code == status.HTTP_200_OK
    

    data = response.json()
    print(data)
    print(order.order_items)
    assert len(data) == 1
    assert data[0]["product_category_name"] == ProductCategoryEnum.BURGERS.name
    assert data[0]["product_name"] == order.order_items[0].product_name

def test_get_order_by_id_and_return_success(client):
    order = OrderFactory()

    response = client.get(f"/api/v1/orders/{order.id}")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["customer"] == order.id_customer
    assert data["order_status"]["status"] == order.order_status.status
    assert data["order_status"]["description"] == order.order_status.description
    assert data['id'] == order.id


def test_add_item_and_return_success(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    order_item = OrderItemFactory(product_category_name=ProductCategoryEnum.BURGERS.name, product_id=1)

    payload = {
        "order_id": order.id,
        "product_id": order_item.product_id,
        "quantity": 1,
        "observation": "No onions"
    }

    response = client.post(
        f"/api/v1/orders/{order.id}/items",
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["detail"] == "Item adicionado com sucesso."

def test_try_add_item_product_with_different_category_and_return_error(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_DRINKS.status, description=OrderStatusEnum.ORDER_WAITING_DRINKS.description)
    order = OrderFactory(order_status=order_status)

    order_item = OrderItemFactory(product_category_name=ProductCategoryEnum.BURGERS.name, product_id=1)

    payload = {
        "order_id": order.id,
        "product_id": order_item.product_id,
        "quantity": 1,
        "observation": "No onions"
    }

    response = client.post(
        f"/api/v1/orders/{order.id}/items",
        json=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert data["detail"]["message"] == "Não é possível adicionar itens da categoria 'burgers' no status atual 'order_waiting_drinks'."


def test_remove_item_and_return_success(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    order_item = OrderItemFactory(order=order, product_category_name=ProductCategoryEnum.BURGERS.name, product_id=1)

    response = client.delete(
        f"/api/v1/orders/{order.id}/items/{order_item.id}",
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Item removido com sucesso."

def test_try_remove_item_from_order_when_item_not_exists_and_return_error(client):
    order = OrderFactory()

    response = client.delete(
        f"/api/v1/orders/{order.id}/items/1",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O item com ID '1' não foi encontrado no pedido."

def test_change_item_quantity_and_return_success(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    order_item = OrderItemFactory(order=order, product_category_name=ProductCategoryEnum.BURGERS.name, product_id=1)

    payload = {
        "order_id": order.id,
        "new_quantity": 2
    }

    response = client.put(
        f"/api/v1/orders/{order.id}/items/{order_item.id}/quantity",
        params={"order_item_id": order_item.id, "new_quantity": 2},
        json=payload,
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Quantidade atualizada com sucesso."

def test_try_change_item_quantity_when_item_not_exists_and_return_error(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    response = client.put(
        f"/api/v1/orders/{order.id}/items/1/quantity",
        params={"order_item_id": 1, "new_quantity": 2},
        json={"order_id": order.id, "new_quantity": 2},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O item com ID '1' não foi encontrado no pedido."

def test_change_item_observation_and_return_success(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    order_item = OrderItemFactory(order=order, product_category_name=ProductCategoryEnum.BURGERS.name)

    payload = {
        "order_id": order.id,
        "new_observation": "No onions"
    }

    response = client.put(
        f"/api/v1/orders/{order.id}/items/{order_item.id}/observation",
        params={"item_id": order_item.id, "new_observation": payload["new_observation"]},
        json=payload,        
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Observação atualizada com sucesso."

def test_try_change_item_observation_when_item_not_exists_and_return_error(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    response = client.put(
        f"/api/v1/orders/{order.id}/items/1/observation",
        params={"item_id": 1, "new_observation": "No onions"},
        json={"order_id": order.id, "new_observation": "No onions"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O item com ID '1' não foi encontrado no pedido."

def test_list_order_items_and_return_success(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    order_item_model = OrderItemFactory(order=order, product_category_name=ProductCategoryEnum.BURGERS.name)

    response = client.get(f"/api/v1/orders/{order.id}/items")

    assert response.status_code == status.HTTP_200_OK

    order_item = order_item_model.to_entity()
    data = response.json()
    assert len(data) == 1
    assert data[0]["product_category_name"] == ProductCategoryEnum.BURGERS.name
    assert data[0]["product_name"] == order_item.product_name
    assert data[0]["quantity"] == order_item.quantity
    assert data[0]["observation"] == order_item.observation
    assert data[0]["total"] == order_item.total

def test_try_list_order_items_when_order_not_exists_and_return_error(client):
    response = client.get("/api/v1/orders/999/items")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."

'''
def test_try_list_order_items_when_order_not_belongs_to_customer_and_return_error(client):
    person = PersonFactory()
    CustomerFactory(person=person)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    response = client.get(
        f"/api/v1/orders/{order.id}/items",
        permissions=[OrderPermissions.CAN_LIST_ORDER_ITEMS],
        profile_name="customer",
        person={
            "id": person.id,
            "cpf": person.cpf,
            "name": person.name,
            "email": person.email,
        }
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '1' não foi encontrado."
'''
def test_go_back_order_status_and_return_success(client):
    OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_SIDES.status, description=OrderStatusEnum.ORDER_WAITING_SIDES.description)
    
    order = OrderFactory(order_status=order_status)

    response = client.post(f"/api/v1/orders/{order.id}/go-back", params={"order_id": order.id})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["order_status"]["status"] == "order_waiting_burgers"

def test_try_go_back_order_status_when_order_not_exists_and_return_error(client):
    response = client.post("/api/v1/orders/999/go-back", params={"order_id": 999})

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."

def test_try_go_back_order_status_when_order_status_is_waiting_burgers_and_return_error(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    response = client.post(f"/api/v1/orders/{order.id}/go-back", params={"order_id": order.id})

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert data["detail"]["message"] == "O status atual 'order_waiting_burgers' não permite voltar."

def test_try_go_back_order_status_when_order_status_is_order_placed_and_return_error(client):    
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_PLACED.status, description=OrderStatusEnum.ORDER_PLACED.description)
    order = OrderFactory(order_status=order_status)

    response = client.post(f"/api/v1/orders/{order.id}/go-back", params={"order_id": order.id})

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data = response.json()
    assert data["detail"]["message"] == "O status atual 'order_placed' não permite voltar."

def test_next_step_order_status_and_return_success(client):    
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_SIDES.status, description=OrderStatusEnum.ORDER_WAITING_SIDES.description)
    
    order = OrderFactory(order_status=order_status)

    response = client.post(
        f"/api/v1/orders/{order.id}/advance",
        params={"order_id": order.id}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['order_status']['status'] == "order_waiting_sides"

def test_try_next_step_order_status_when_order_not_exists_and_return_error(client):
    response = client.post("/api/v1/orders/999/advance", params={"order_id": 999})

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."

def test_clear_order_and_return_success(client):    
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    response = client.delete(f"/api/v1/orders/{order.id}/clear", params={"order_id": order.id})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Pedido limpo com sucesso."
    
def test_try_clear_order_when_order_not_exists_and_return_error(client):
    response = client.delete("/api/v1/orders/999/clear", params={"order_id": 999})

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."

def test_cancel_order_and_return_success(client):
    order_status = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status)

    OrderStatusFactory(status=OrderStatusEnum.ORDER_CANCELLED.status, description=OrderStatusEnum.ORDER_CANCELLED.description)

    response = client.post(f"/api/v1/orders/{order.id}/cancel", params={"order_id": order.id})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["detail"] == "Pedido cancelado com sucesso."
    
def test_try_cancel_order_when_order_not_exists_and_return_error(client):
    response = client.post("/api/v1/orders/999/cancel", params={"order_id": 999})
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert data["detail"]["message"] == "O pedido com ID '999' não foi encontrado."

@pytest.mark.parametrize("order_status", [
    OrderStatusEnum.ORDER_WAITING_BURGERS,
    OrderStatusEnum.ORDER_WAITING_SIDES,
    OrderStatusEnum.ORDER_WAITING_DRINKS,
    OrderStatusEnum.ORDER_WAITING_DESSERTS
])
def test_list_orders_and_return_success(order_status, client):
    order_status_waiting_sandwich = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order_status_waiting_sides = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_SIDES.status, description=OrderStatusEnum.ORDER_WAITING_SIDES.description)
    order_status_waiting_drinks = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_DRINKS.status, description=OrderStatusEnum.ORDER_WAITING_DRINKS.description)
    order_status_waiting_desserts = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_DESSERTS.status, description=OrderStatusEnum.ORDER_WAITING_DESSERTS.description)
    
    OrderFactory(order_status=order_status_waiting_sandwich)
    OrderFactory(order_status=order_status_waiting_sides)
    OrderFactory(order_status=order_status_waiting_drinks)
    OrderFactory(order_status=order_status_waiting_desserts)

    response = client.get("/api/v1/orders", params={"status": order_status.status})

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] is not None
    assert data[0]["order_status"]["status"] == order_status.status
    assert data[0]["order_status"]["description"] == order_status.description
    
@pytest.mark.parametrize("order_status", [OrderStatusEnum.ORDER_WAITING_BURGERS,])
def test_get_order_status_success(client, order_status):
    order_status_waiting_burger = OrderStatusFactory(status=OrderStatusEnum.ORDER_WAITING_BURGERS.status, description=OrderStatusEnum.ORDER_WAITING_BURGERS.description)
    order = OrderFactory(order_status=order_status_waiting_burger)

    res = client.get(f'api/v1/orders/{order.id}/status',)
    assert res.status_code == status.HTTP_200_OK

    data = res.json()
    assert data['status'] == order.order_status.status
