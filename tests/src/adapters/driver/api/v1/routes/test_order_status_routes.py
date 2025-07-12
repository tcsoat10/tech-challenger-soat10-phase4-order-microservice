from fastapi import status

import pytest

from tests.factories.order_status_factory import OrderStatusFactory
from src.constants.permissions import OrderStatusPermissions


@pytest.mark.parametrize("payload", [
    {"status": "ATIVO", "description": "TESTE DE STATUS ATIVO"},
    {"status": "INATIVO", "description": "TESTE DE STATUS INATIVO"},
])

def test_create_order_status_success(client, db_session, payload):
    response = client.post("/api/v1/order_status", json=payload, permissions=[OrderStatusPermissions.CAN_CREATE_ORDER_STATUS])

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["status"] == payload["status"]
    assert data["description"] == payload["description"]

def test_create_order_status_duplicate_status_and_return_error(client, db_session):
    OrderStatusFactory(status="ATIVO")

    payload = {
        "status": "ATIVO",
        "description": "TESTE DE STATUS ATIVO"
    }

    response = client.post("/api/v1/order_status", json=payload, permissions=[OrderStatusPermissions.CAN_CREATE_ORDER_STATUS])
    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()
    assert data["detail"]["message"] == "OrderStatus already exists."

def test_get_order_status_by_status_and_return_success(client):
    OrderStatusFactory(
        status="ATIVO",
        description="TESTE DE STATUS ATIVO"
    )
    OrderStatusFactory(
        status="INATIVO",
        description="TESTE DE STATUS INATIVO"
    )
    
    response = client.get("/api/v1/order_status/ATIVO/status", permissions=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["status"] == "ATIVO"
    assert data["description"] == "TESTE DE STATUS ATIVO"

def test_get_order_status_by_id_and_return_success(client):
    order_status1 = OrderStatusFactory(
        status="ATIVO",
        description="TESTE DE STATUS ATIVO"
    )
    OrderStatusFactory(
        status="INATIVO",
        description="TESTE DE STATUS INATIVO"
    )
    
    response = client.get(f"/api/v1/order_status/{order_status1.id}/id", permissions=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "id" in data
    assert data["status"] == "ATIVO"
    assert data["description"] == "TESTE DE STATUS ATIVO"

def test_get_all_order_status_return_success(client):
    order_status1 = OrderStatusFactory(
        status="ATIVO",
        description="TESTE DE STATUS ATIVO"
    )
    order_status2 = OrderStatusFactory(
        status="INATIVO",
        description="TESTE DE STATUS INATIVO"
    )
    
    response = client.get("/api/v1/order_status", permissions=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            "id": order_status1.id,
            "status": order_status1.status,
            "description": order_status1.description
        },
        {
            "id": order_status2.id,
            "status": order_status2.status,
            "description": order_status2.description
        }
    ]

def test_update_order_status_and_return_success(client):
    order_status = OrderStatusFactory(
        status="ATIVO",
        description="TESTE DE STATUS ATIVO"
    )
    
    payload = {
        "id": 1,
        "status": "ATIVO - UPD",
        "description": "TESTE DE STATUS ATIVO - UPDATED"
    }

    response = client.put(f"/api/v1/order_status/{order_status.id}", json=payload, permissions=[OrderStatusPermissions.CAN_UPDATE_ORDER_STATUS])

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "id": order_status.id,
        "status": "ATIVO - UPD",
        "description": "TESTE DE STATUS ATIVO - UPDATED"
    }

def test_delete_order_status_and_return_success(client):
    order_status1 = OrderStatusFactory(status="ATIVO", description="TESTE DE STATUS ATIVO")
    order_status2 = OrderStatusFactory(status="INATIVO", description="TESTE DE STATUS INATIVO")

    response = client.delete(f"/api/v1/order_status/{order_status1.id}", permissions=[OrderStatusPermissions.CAN_DELETE_ORDER_STATUS])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get("/api/v1/order_status", permissions=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data == [{
        "id": order_status2.id,
        "status": order_status2.status,
        "description": order_status2.description
    }]