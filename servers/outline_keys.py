from config import outline_client
from database.controllers.key import create_key, get_order_country_key


def get_key(country: str, order_id: int) -> str:
    key = get_order_country_key(country=country, order_id=order_id)
    if key is not None:
        return key.key

    new_key = outline_client[country].create_key().access_url
    create_key({"order_id": order_id, "country": country, "key": new_key})
    return new_key
