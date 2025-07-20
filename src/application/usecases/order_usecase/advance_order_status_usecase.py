
from src.constants.order_transition import STATUS_ALLOWED_ACCESS_ONLY_CUSTOMER, STATUS_ALLOWED_ACCESS_ONLY_EMPLOYEE
from src.core.domain.entities.order import Order
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.constants.order_status import OrderStatusEnum
from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO


class AdvanceOrderStatusUseCase:
    def __init__(
            self,
            order_gateway: IOrderRepository,
            order_status_gateway: IOrderStatusRepository,
            payment_gateway: IPaymentProviderGateway
    ):
        self.order_gateway = order_gateway
        self.order_status_gateway = order_status_gateway
        self.payment_gateway = payment_gateway

    @classmethod
    def build(
        cls,
        order_gateway: IOrderRepository,
        order_status_gateway: IOrderStatusRepository,
        payment_gateway: IPaymentProviderGateway
    ) -> 'AdvanceOrderStatusUseCase':
        return cls(order_gateway, order_status_gateway, payment_gateway)

    def execute(self, order_id: int) -> Order:
        order = self.order_gateway.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")

        #order.advance_order_status(self.order_status_gateway, employee=employee)
        order.advance_order_status(self.order_status_gateway)
        order = self.order_gateway.update(order)

        if order.order_status.status == OrderStatusEnum.ORDER_PLACED.status:
            payment_dto = CreatePaymentDTO(
                title=f"order-{order.id}",
                description=f"Pagamento do pedido #{order.id}",
                payment_method="qr_code",
                total_amount=order.total,
                currency="BRL",
                notification_url="https://example.com/callback",
                items=order.order_items,
                customer=order.id_customer,
            )
            payment_id = self.payment_gateway.create_payment(payment_dto)
            order.payment_id = payment_id
            order = self.order_gateway.update(order)

        return order