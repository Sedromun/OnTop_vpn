from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from logs import bot_logger
from schemas import OrderModel
from schemas.key import KeyModel


def get_key(key_id: int) -> KeyModel | None:
    try:
        key = session.scalar(select(KeyModel).where(KeyModel.id == key_id))
        return key
    except IntegrityError:
        session.rollback()
        return None


def get_order_country_key(order: OrderModel, country: str) -> KeyModel | None:
    keys = order.keys

    for key in keys:
        if key.country == country:
            return key
    return None


def create_key(data: dict) -> KeyModel | None:
    key = KeyModel(**data)

    try:
        session.add(key)
        session.commit()
        bot_logger.info("key '" + str(key.id) + "' successfully created!")
        return key
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            "Integrity error in create_key - can't commit in db", exc_info=e
        )
        return None


def update_key(key_id: int, updates: dict) -> bool:
    try:
        session.query(KeyModel).filter(KeyModel.id == key_id).update(updates)
        session.commit()
        bot_logger.info("key '" + str(key_id) + "' successfully updated!")
        return True
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            "Integrity error in update_key - can't commit in db", exc_info=e
        )
        return False


def delete_key(key_id: int) -> bool:
    try:
        session.query(KeyModel).filter(KeyModel.id == key_id).delete()
        session.commit()
        bot_logger.info("KeyModel" + " '" + str(key_id) + "' successfully deleted!")
        return True
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            "Integrity error in delete_key 'KeyModel' - can't commit in db", exc_info=e
        )
        return False


def get_server_id_usages(server_id: int) -> int:
    try:
        keys = session.scalars(select(KeyModel).where(KeyModel.server_id == server_id)).all()
        return len(keys)
    except IntegrityError:
        session.rollback()
        return None


def get_zero_id_usage(server_id: int, country: str) -> int:
    try:
        keys = session.scalars(select(KeyModel).where(KeyModel.country == country)).all()
        cnt = 0
        for key in keys:
            if key.server_id is None or key.server_id == server_id or key.server_id == 0:
                cnt += 1
        return cnt
    except IntegrityError:
        session.rollback()
        return None
