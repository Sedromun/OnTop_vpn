from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session
from logs import Logger
from schemas import OrderModel


def get_order(order_id: int) -> OrderModel | None:
    order = session.scalar(select(OrderModel).where(OrderModel.id == order_id))
    return order


def create_order(data: dict) -> OrderModel | None:
    order = OrderModel(**data)

    session.add(order)

    try:
        session.commit()
        Logger.info("order '" + str(order.id) + "' successfully created!")
        return order
    except IntegrityError as e:
        session.rollback()
        Logger.exception(e, "Integrity error in create_order - can't commit in db")
        return None


def update_order(order_id: int, updates: dict) -> bool:
    session.query(OrderModel).filter(OrderModel.id == order_id).update(updates)

    try:
        session.commit()
        Logger.info("order '" + str(order_id) + "' successfully updated!")
        return True
    except IntegrityError as e:
        session.rollback()
        Logger.exception(e, "Integrity error in update_order - can't commit in db")
        return False


def delete_order(order_id: int, model_name: str) -> bool:
    session.query(OrderModel).filter(OrderModel.id == order_id).delete()

    try:
        session.commit()
        Logger.info(model_name + " '" + str(order_id) + "' successfully deleted!")
        return True
    except IntegrityError as e:
        session.rollback()
        Logger.exception(
            e, f"Integrity error in delete_order '{model_name}' - can't commit in db"
        )
        return False
