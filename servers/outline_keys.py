from config import outline_client
from database.controllers.key import create_key, get_order_country_key
from database.controllers.order import update_order, get_order


def get_key(country: str, order_id: int) -> str:
    order = get_order(order_id)
    key = get_order_country_key(country=country, order=order)
    if key is not None:
        return key.key

    new_key = outline_client[country].create_key().access_url
    create_key({"order_id": order_id, "country": country, "key": new_key})
    return new_key
