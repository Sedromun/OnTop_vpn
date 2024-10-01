from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from logs import Logger
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
        Logger.info("key '" + str(key.id) + "' successfully created!")
        return key
    except IntegrityError as e:
        session.rollback()
        Logger.exception(e, "Integrity error in create_key - can't commit in db")
        return None


def update_key(key_id: int, updates: dict) -> bool:
    try:
        session.query(KeyModel).filter(KeyModel.id == key_id).update(updates)
        session.commit()
        Logger.info("key '" + str(key_id) + "' successfully updated!")
        return True
    except IntegrityError as e:
        session.rollback()
        Logger.exception(e, "Integrity error in update_key - can't commit in db")
        return False


def delete_key(key_id: int) -> bool:
    try:
        session.query(KeyModel).filter(KeyModel.id == key_id).delete()
        session.commit()
        Logger.info("KeyModel" + " '" + str(key_id) + "' successfully deleted!")
        return True
    except IntegrityError as e:
        session.rollback()
        Logger.exception(
            e, "Integrity error in delete_key 'KeyModel' - can't commit in db"
        )
        return False
