from config import outline_client
from database.controllers.key import get_order_country_key, create_key
from database.controllers.order import get_order
from outline.outline_vpn.outline_vpn import OutlineVPN
from schemas.key import KeyModel


def get_key(country: str, order_id: int) -> str:
    key = get_order_country_key(country=country, order_id=order_id)
    if key is not None:
        return key.key

    new_key = outline_client[country].create_key()
    create_key({
        "order_id": order_id,
        "country": country,
        "key": new_key
    })
    return new_key


