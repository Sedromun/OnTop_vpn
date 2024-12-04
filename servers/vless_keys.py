import datetime
import uuid

from config import outline_client, country_to_server_ids, efficiency, vless_client, servers_countries_in_email, \
    vless_server_ip, parameters, vless_inbound_id
from database.controllers.key import (create_key, delete_key,
                                      get_order_country_key, get_server_id_usages, get_zero_id_usage)
from database.controllers.key import get_key as get_key_from_db
from database.controllers.order import get_order, update_order
from py3xui.client.client import Client
from utils.country import fastest


async def get_vless_keys(order_id: int) -> str:
    res = ""
    for id, api in vless_client.items():
        email = servers_countries_in_email[id] + "-" + str(order_id)
        order = get_order(order_id)
        await api.login()
        client = await api.client.get_by_email(email)

        if client is None:
            if order.uuid is None:
                uid = str(uuid.uuid4())
                update_order(order_id, {"uuid": uid})
            else:
                uid = order.uuid

            client = Client(
                id=uid,
                email=email,
                enable=True,
                flow="xtls-rprx-vision"
            )
            await api.client.add(vless_inbound_id[id], [client])

        order = get_order(order_id)
        res += create_key_string_from_data(id, order.uuid, client) + '\n'
    return res


def create_key_string_from_data(server_id: str, uid: str, client: Client) -> str:
    res = f"vless://{uid}@{vless_server_ip[server_id]}:443?"
    for name, val in parameters[server_id].items():
        res += f"{name}={val}"
        if name != "flow":
            res += "&"
        else:
            res += "#"
    res += "clique-vpn-" + client.email
    return res
