from config import outline_client, country_to_server_ids
from database.controllers.key import (create_key, delete_key,
                                      get_order_country_key)
from database.controllers.order import get_order


def get_key(country: str, order_id: int) -> str:
    order = get_order(order_id)
    key = get_order_country_key(country=country, order=order)
    if key is not None:
        delete_key(key.id)

    new_key = get_client(country).create_key().access_url
    create_key({"order_id": order_id, "country": country, "key": new_key})
    return new_key


def get_client(country: str):
    server_ids = country_to_server_ids[country]
    # mn_id = server_ids[0]
    # mn = 100000000
    #
    # for i in range(len(server_ids)):
    #     cur_id = server_ids[i]
    return outline_client[server_ids[0]]
