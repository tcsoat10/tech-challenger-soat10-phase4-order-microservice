
from fastapi import APIRouter, status, Depends
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.webhook_controller import WebhookController
from src.core.domain.dtos.webhook.payment_webhook_dto import PaymentWebhookDTO
from src.core.containers import Container

router = APIRouter()

@router.post(
    "/webhook/payment_notification",
    status_code=status.HTTP_200_OK,
)
@inject
async def payment_notification(
    dto: PaymentWebhookDTO,
    controller: WebhookController = Depends(Provide[Container.webhook_controller]),
):
    await controller.handle_payment_notification(dto)
    return {"status": "success"}
