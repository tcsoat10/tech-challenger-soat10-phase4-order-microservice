from src.application.usecases.webhook_usecase.approval_payment_usecase import ApprovalPaymentUseCase
from src.core.domain.dtos.webhook.payment_webhook_dto import PaymentWebhookDTO
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway


class WebhookController:

    def __init__(
        self,
        order_gateway: IOrderRepository,
        order_status_gateway: IOrderStatusRepository,
        payment_gateway: IPaymentProviderGateway
    ):
        self.order_gateway: IOrderRepository = order_gateway
        self.order_status_gateway: IOrderStatusRepository = order_status_gateway
        self.payment_gateway: IPaymentProviderGateway = payment_gateway

    async def handle_payment_notification(self, dto: PaymentWebhookDTO) -> None:
        approval_payment_usecase: ApprovalPaymentUseCase = ApprovalPaymentUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway,
            payment_gateway=self.payment_gateway
        )
        approval_payment_usecase.execute(payment_id=dto.payment_id, payment_status=dto.status)
