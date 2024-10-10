from typing import Type

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from logs import bot_logger
from schemas import OrderModel, FinishedOrderModel


def get_order(order_id: int) -> OrderModel | None:
    order = session.scalar(select(OrderModel).where(OrderModel.id == order_id))
    return order


def get_all_orders(model: Type[OrderModel | FinishedOrderModel] = OrderModel) -> list[OrderModel | FinishedOrderModel]:
    orders = session.scalars(select(model)).all()
    return orders


def get_all_country_orders(country: str) -> list[OrderModel]:
    orders = session.scalars(
        select(OrderModel).where(OrderModel.country == country)
    ).all()
    return orders


def create_order(data: dict, model: Type[OrderModel | FinishedOrderModel] = OrderModel) -> OrderModel | None:
    order = model(**data)

    session.add(order)

    try:
        session.commit()
        bot_logger.info("order '" + str(order.id) + "' successfully created!, model: " + str(model))
        return order
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            "Integrity error in create_order - can't commit in db", exc_info=e
        )
        return None


def update_order(order_id: int, updates: dict) -> bool:
    try:
        session.query(OrderModel).filter(OrderModel.id == order_id).update(updates)
        session.commit()
        bot_logger.info("order '" + str(order_id) + "' successfully updated!")
        return True
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            "Integrity error in update_order - can't commit in db", exc_info=e
        )
        return False


def delete_order(order_id: int) -> bool:
    try:
        session.query(OrderModel).filter(OrderModel.id == order_id).delete()
        session.commit()
        bot_logger.info("OrderModel '" + str(order_id) + "' successfully deleted!")
        return True
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            f"Integrity error in delete_order 'OrderModel' - can't commit in db",
            exc_info=e,
        )
        return False
