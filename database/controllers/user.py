from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from logs import bot_logger
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


def get_all_users() -> list[UserModel]:
    users = session.scalars(select(UserModel)).all()
    return users


def get_user(tg_id: int) -> UserModel | None:
    user = session.scalar(select(UserModel).where(UserModel.id == tg_id))
    return user


def register_user(tg_id: int) -> UserModel | None:
    creating_user = UserModel(id=tg_id)

    session.add(creating_user)

    try:
        session.commit()
        bot_logger.info("User '" + str(tg_id) + "' successfully created!")
        return creating_user
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            f"Integrity error in register_user '{str(tg_id)}' - can't commit in db",
            exc_info=e,
        )
        return None


def update_user(tg_id: int, updates: dict) -> bool:
    session.query(UserModel).filter(UserModel.id == tg_id).update(updates)
    try:
        session.commit()
        bot_logger.info("User '" + str(tg_id) + "' successfully updated!")
        return True
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            f"Integrity error in update_user '{str(tg_id)}' - can't commit in db",
            exc_info=e,
        )
        return False


def get_referrals(user_id: int):
    return session.scalars(
        select(UserModel).where(UserModel.referrer_id == user_id)
    ).all()
