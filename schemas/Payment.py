from pydantic import BaseModel


class PaymentSchema(BaseModel):
    id: str
    status: str
    paid: bool
    amount: dict
    authorization_details: dict
    created_at: str
    description: str
    expires_at: str
    metadata: dict
    payment_method: dict
    recipient: dict
    refundable: bool
    test: bool
    income_amount: dict
