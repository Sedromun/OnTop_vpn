from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from logs import Logger
from schemas import OrderModel, UserModel


def get_user_orders(tg_id: int) -> list[OrderModel] | None:
    user = session.scalar(select(UserModel).where(UserModel.id == tg_id))
    orders = user.orders
    res = []
    for order in orders:
        if order.keys:
            res.append(order)
    res.sort(key=lambda x: x.id)
    return res


def get_user(tg_id: int) -> UserModel | None:
    user = session.scalar(select(UserModel).where(UserModel.id == tg_id))
    return user


def register_user(tg_id: int) -> UserModel  | None:
    creating_user = UserModel(id=tg_id)

    session.add(creating_user)

    try:
        session.commit()
        Logger.info("User '" + str(tg_id) + "' successfully created!")
        return creating_user
    except IntegrityError as e:
        session.rollback()
        Logger.exception(e, f"Integrity error in register_user '{str(tg_id)}' - can't commit in db")
        return None


def update_user(tg_id: int, updates: dict) -> bool:
    session.query(UserModel).filter(UserModel.id == tg_id).update(updates)
    try:
        session.commit()
        Logger.info("User '" + str(tg_id) + "' successfully updated!")
        return True
    except IntegrityError as e:
        session.rollback()
        Logger.exception(e, f"Integrity error in update_user '{str(tg_id)}' - can't commit in db")
        return False
