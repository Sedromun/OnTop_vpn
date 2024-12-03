import uuid

from config import outline_client, country_to_server_ids, efficiency, vless_client, servers_countries_in_email, \
    VLESS_INBOUND_ID, vless_server_ip, parameters
from database.controllers.key import (create_key, delete_key,
                                      get_order_country_key, get_server_id_usages, get_zero_id_usage)
from database.controllers.key import get_key as get_key_from_db
from database.controllers.order import get_order
from py3xui.py3xui.client.client import Client
from utils.country import fastest


def get_vless_keys(order_id: int) -> str:
    res = ""
    for id, api in vless_client.items():
        email = servers_countries_in_email[id] + "-" + str(order_id)
        client = api.client.get_by_email(email)
        order = get_order(order_id)

        if client is None:
            client = Client(
                id=str(uuid.uuid4()),
                email=email,
                enable=True,
                flow="xtls-rprx-vision",
            )
            api.client.add(VLESS_INBOUND_ID, [client])
        res += create_key_string_from_data(id, client) + '\n'
    return res


def create_key_string_from_data(server_id: str, client: Client) -> str:
    res = f"vless://{client.id}@{vless_server_ip[server_id]}:443?"
    for name, val in parameters[server_id].items():
        res += f"{name}={val}"
        if name != "spx":
            res += "&"
        else:
            res += "#"
    res += "clique-vpn-" + client.email
    return res
