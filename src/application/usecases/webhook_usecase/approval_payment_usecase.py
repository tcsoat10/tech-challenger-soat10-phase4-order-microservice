
from src.constants.order_status import OrderStatusEnum
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.constants.payment_status import PaymentStatusEnum
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository


class ApprovalPaymentUseCase:
    def __init__(
        self,
        order_gateway: IOrderRepository,
        order_status_gateway: IOrderStatusRepository,
        payment_gateway: IPaymentProviderGateway
    ):
        self.order_repository = order_gateway
        self.order_status_gateway = order_status_gateway
        self.payment_gateway = payment_gateway
        
    @classmethod
    def build(
        cls,
        order_gateway: IOrderRepository,
        order_status_gateway: IOrderStatusRepository,
        payment_gateway: IPaymentProviderGateway
    ) -> 'ApprovalPaymentUseCase':
        return cls(order_gateway, order_status_gateway, payment_gateway)

    def execute(self, payment_id: int, payment_status: str) -> None:
        order = self.order_repository.get_by_payment_id(payment_id)
        if not order:
            # if payment_status == PaymentStatusEnum.PAYMENT_COMPLETED.status:
            #     self.payment_gateway.refund_payment(payment_id)
            raise EntityNotFoundException(f"Order with payment ID {payment_id} not found.")
        
        if order.order_status.status != OrderStatusEnum.ORDER_PLACED.status:
            raise EntityNotFoundException(f"Order with ID {order.id} is not in the 'ORDER_PLACED' status.")
        
        if payment_status != PaymentStatusEnum.PAYMENT_COMPLETED.status:
            raise EntityNotFoundException(f"Payment with ID {payment_id} is not completed.")

        # if payment_status == PaymentStatusEnum.PAYMENT_FAILED.status:
        #     self.payment_gateway.refund_payment(payment_id)
        
        if (
            order.order_status.status == OrderStatusEnum.ORDER_PLACED.status and
            payment_status == PaymentStatusEnum.PAYMENT_COMPLETED.status
        ):
            order.advance_order_status(self.order_status_gateway)
            self.order_repository.update(order)
        else:
            raise EntityNotFoundException(f"Payment with ID {payment_id} is not completed or order status is not 'ORDER_PLACED'.")
