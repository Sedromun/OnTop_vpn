from config import outline_client, country_to_server_ids, efficiency
from database.controllers.key import (create_key, delete_key,
                                      get_order_country_key, get_server_id_usages, get_zero_id_usage)
from database.controllers.key import get_key as get_key_from_db
from database.controllers.order import get_order
from utils.country import fastest


def get_key(country: str, order_id: int) -> str:
    order = get_order(order_id)
    key = get_order_country_key(country=country, order=order)
    if key is not None:
        delete_key(key.id)

    server_id, _, client = get_client(country)
    new_key = client.create_key().access_url
    create_key({"order_id": order_id, "country": country, "server_id": server_id, "key": new_key})
    return new_key


def get_client(country: str):
    if country == fastest:
        mn_id = -1
        mn = 10000000
        for cntr in country_to_server_ids.keys():
            cur_id, cur, _ = get_country_client(cntr)
            if cur < mn:
                mn = cur
                mn_id = cur_id
        return mn_id, mn, outline_client[mn_id]
    else:
        return get_country_client(country)

def get_country_client(country: str):
    server_ids = country_to_server_ids[country]
    mn_id = server_ids[0]
    mn = get_zero_id_usage(mn_id, country)

    for i in range(1, len(server_ids)):
        cur_id = server_ids[i]
        num_usages = get_server_id_usages(cur_id)
        if num_usages is not None and num_usages / efficiency[cur_id] < mn:
            mn = num_usages / efficiency[cur_id]
            mn_id = cur_id

    return mn_id, mn, outline_client[mn_id]
