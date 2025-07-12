from fastapi import status

from src.core.exceptions.utils import ErrorCode
from tests.factories.order_factory import OrderFactory
from tests.factories.product_factory import ProductFactory
from tests.factories.order_item_factory import OrderItemFactory
from src.constants.permissions import OrderItemPermissions

def test_create_order_item_success(client, db_session):
    product = ProductFactory(name="Burger", price=10.0)
    order = OrderFactory()
    payload = {
        "order_id": order.id,
        "product_id": product.id,
        "quantity": 2,
        "observation": "No onions",
    }

    response = client.post("/api/v1/order-items", json=payload, permissions=[OrderItemPermissions.CAN_CREATE_ORDER_ITEM])

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["product"]['name'] == product.name
    assert data["quantity"] == payload["quantity"]
    assert data["observation"] == payload["observation"]
    assert data["total"] == product.price * payload["quantity"]

def test_create_order_item_with_invalid_product_id(client, db_session):
    order = OrderFactory()
    payload = {
        "order_id": order.id,
        "product_id": 1,
        "quantity": 2,
        "observation": "No onions",
    }

    response = client.post("/api/v1/order-items", json=payload, permissions=[OrderItemPermissions.CAN_CREATE_ORDER_ITEM])

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Product not found.',
            'details': None,
        }
    }

def test_get_order_item_by_id_success(client, db_session):
    order_item_model = OrderItemFactory()
    response = client.get(f"/api/v1/order-items/{order_item_model.id}/id", permissions=[OrderItemPermissions.CAN_VIEW_ORDER_ITEMS])

    assert response.status_code == status.HTTP_200_OK

    order_item = order_item_model.to_entity()
    data = response.json()

    assert data["id"] == order_item.id
    assert data["product"]["id"] == order_item.product.id
    assert data["quantity"] == order_item.quantity
    assert data["observation"] == order_item.observation
    assert data["total"] == order_item.total


def test_get_order_item_by_id_with_invalid_id(client, db_session):
    response = client.get("/api/v1/order-items/1/id", permissions=[OrderItemPermissions.CAN_VIEW_ORDER_ITEMS])

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Order Item not found.',
            'details': None,
        }
    }

def test_get_all_order_items_success(client, db_session):
    order_item1 = OrderItemFactory()
    order_item2 = OrderItemFactory()

    response = client.get("/api/v1/order-items", permissions=[OrderItemPermissions.CAN_VIEW_ORDER_ITEMS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == order_item1.id
    assert data[1]["id"] == order_item2.id

def test_get_all_order_items_with_empty_db(client, db_session):
    response = client.get("/api/v1/order-items", permissions=[OrderItemPermissions.CAN_VIEW_ORDER_ITEMS])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data == []

def test_update_order_item_success(client, db_session):
    order_item = OrderItemFactory(quantity=1, observation="No onions")
    order = OrderFactory(order_items=[order_item])

    payload = {
        "id": order_item.id,
        "order_id": order.id,
        "product_id": order_item.product_id,
        "quantity": 3,
        "observation": "No onions, please.",
    }

    response = client.put(f"/api/v1/order-items/{order_item.id}", json=payload, permissions=[OrderItemPermissions.CAN_UPDATE_ORDER_ITEM])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert data["id"] == order_item.id
    assert data["product"]["id"] == order_item.product_id
    assert data["quantity"] == payload["quantity"]
    assert data["observation"] == payload["observation"]
    assert data["total"] == order_item.product.price * payload["quantity"]

def test_update_order_item_with_invalid_product_id(client, db_session):
    order_item = OrderItemFactory(product__id=1)
    order = OrderFactory(order_items=[order_item])

    payload = {
        "id": order_item.id,
        "order_id": order.id,
        "product_id": 5,
        "quantity": 3,
        "observation": "No onions, please.",
    }

    response = client.put(f"/api/v1/order-items/{order_item.id}", json=payload, permissions=[OrderItemPermissions.CAN_UPDATE_ORDER_ITEM])

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Product not found.',
            'details': None,
        }
    }

def test_update_order_item_with_invalid_order_item_id(client, db_session):
    payload = {
        "id": 1,
        "order_id": 1,
        "product_id": 1,
        "quantity": 3,
        "observation": "No onions, please.",
    }

    response = client.put("/api/v1/order-items/1", json=payload, permissions=[OrderItemPermissions.CAN_UPDATE_ORDER_ITEM])

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Order Item not found.',
            'details': None,
        }
    }

def test_delete_order_item_success(client, db_session):
    order_item = OrderItemFactory()

    response = client.delete(f"/api/v1/order-items/{order_item.id}", permissions=[OrderItemPermissions.CAN_DELETE_ORDER_ITEM])

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_order_item_with_invalid_id(client, db_session):
    response = client.delete("/api/v1/order-items/1", permissions=[OrderItemPermissions.CAN_DELETE_ORDER_ITEM])

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Order Item not found.',
            'details': None,
        }
    }

def test_delete_order_item_twice(client, db_session):
    order_item = OrderItemFactory()

    response = client.delete(f"/api/v1/order-items/{order_item.id}", permissions=[OrderItemPermissions.CAN_DELETE_ORDER_ITEM])

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.delete(f"/api/v1/order-items/{order_item.id}", permissions=[OrderItemPermissions.CAN_DELETE_ORDER_ITEM])

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'Order Item not found.',
            'details': None,
        }
    }

