from enum import Enum

class PaymentStatusEnum(Enum):
    PAYMENT_PENDING = ("payment_pending", "The payment is pending.")
    PAYMENT_COMPLETED = ("payment_completed", "The payment has been completed.")
    PAYMENT_FAILED = ("payment_failed", "The payment has failed.")
    PAYMENT_CANCELLED = ("payment_cancelled", "The payment has been cancelled.")
    PAYMENT_REFUNDED = ("payment_refunded", "The payment has been refunded.")
    PAYMENT_PARTIALLY_REFUNDED = ("payment_partially_refunded", "The payment has been partially refunded.")

    @property
    def status(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    @classmethod
    def values_and_descriptions(cls):
        return [{"name": member.status, "description": member.description} for member in cls]
