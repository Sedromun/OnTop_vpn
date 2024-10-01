from pydantic import BaseModel


class NotificationSchema(BaseModel):
    type: str
    event: str
    object: dict
