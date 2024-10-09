from config import FERNET, KEYS_URL


def get_order_perm_key(order_id: int) -> str:
    to_encrypt = str(order_id)
    order_id_enc = FERNET.encrypt(to_encrypt.encode())
    return KEYS_URL + order_id_enc.decode()
