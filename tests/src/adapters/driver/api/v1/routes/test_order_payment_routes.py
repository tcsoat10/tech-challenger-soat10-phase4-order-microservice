# from tests.factories.order_factory import OrderFactory
# from tests.factories.payment_factory import PaymentFactory
# from src.constants.permissions import OrderPaymentPermissions
# from tests.factories.order_payment_factory import OrderPaymentFactory

# from fastapi import status


# def test_create_order_payment_success(client):
#     order = OrderFactory()
#     payment = PaymentFactory()
#     payload = {'order_id': order.id, 'payment_id': payment.id}

#     response = client.post('/api/v1/order_payments', json=payload, permissions=[OrderPaymentPermissions.CAN_CREATE_ORDER_PAYMENT])
#     assert response.status_code == status.HTTP_201_CREATED

#     data = response.json()
#     assert 'id' in data
#     assert data['order']['id'] == order.id
#     assert data['payment']['id'] == payment.id    


# def test_get_order_payment_by_id_success(client):
#     order_payment = OrderPaymentFactory()

#     response = client.get(
#         f'/api/v1/order_payments/{order_payment.id}/id', permissions=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS]
#     )
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert data['id'] == order_payment.id
#     assert data['order']['id'] == order_payment.order_id
#     assert data['payment']['id'] == order_payment.payment_id


# def test_get_order_payment_by_order_id_success(client):
#     order_payment = OrderPaymentFactory()

#     response = client.get(
#         f'/api/v1/order_payments/{order_payment.order_id}/order_id',
#         permissions=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS]
#     )
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert data['id'] == order_payment.id
#     assert data['order']['id'] == order_payment.order_id
#     assert data['payment']['id'] == order_payment.payment_id


# def test_get_order_payment_by_payment_id_success(client):
#     order_payment = OrderPaymentFactory()

#     response = client.get(
#         f'/api/v1/order_payments/{order_payment.payment_id}/payment_id',
#         permissions=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS]
#     )
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert data['id'] == order_payment.id
#     assert data['order']['id'] == order_payment.order_id
#     assert data['payment']['id'] == order_payment.payment_id


# def test_get_all_order_payments_success(client):
#     order_payment1 = OrderPaymentFactory()
#     order_payment2 = OrderPaymentFactory()

#     response = client.get('/api/v1/order_payments', permissions=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS])
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert len(data) == 2
#     assert data[0]['id'] == order_payment1.id
#     assert data[0]['order']['id'] == order_payment1.order_id
#     assert data[0]['payment']['id'] == order_payment1.payment_id
#     assert data[1]['id'] == order_payment2.id
#     assert data[1]['order']['id'] == order_payment2.order_id
#     assert data[1]['payment']['id'] == order_payment2.payment_id


# def test_update_order_payment_success(client):
#     order_payment = OrderPaymentFactory()
#     order = OrderFactory()
#     payment = PaymentFactory()

#     payload = {'id': order_payment.id, 'order_id': order.id, 'payment_id': payment.id}

#     response = client.put(
#         f'/api/v1/order_payments/{order_payment.id}',
#         json=payload,
#         permissions=[OrderPaymentPermissions.CAN_UPDATE_ORDER_PAYMENT]
#     )
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert data['id'] == order_payment.id
#     assert data['order']['id'] == order.id
#     assert data['payment']['id'] == payment.id


# def test_delete_order_payment_success(client):
#     order_payment = OrderPaymentFactory()
#     order_payment_delete = OrderPaymentFactory()

#     response = client.delete(
#         f'/api/v1/order_payments/{order_payment_delete.id}',
#         permissions=[OrderPaymentPermissions.CAN_DELETE_ORDER_PAYMENT]
#     )
#     assert response.status_code == status.HTTP_204_NO_CONTENT

#     response = client.get('/api/v1/order_payments', permissions=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS])
#     assert response.status_code == status.HTTP_200_OK

#     data = response.json()
#     assert len(data) == 1
#     assert data[0]['id'] == order_payment.id
#     assert data[0]['order']['id'] == order_payment.order_id
#     assert data[0]['payment']['id'] == order_payment.payment_id