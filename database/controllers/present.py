from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from database import session
from logs import bot_logger
from schemas.present import PresentsModel


def create_present_db(data: dict) -> PresentsModel | None:
    order = PresentsModel(**data)

    session.add(order)

    try:
        session.commit()
        bot_logger.info(
            "present '" + str(order.id) + "' successfully created!,"
        )
        return order
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            "Integrity error in create_present_db - can't commit in db", exc_info=e
        )
        return None


def get_present(present_id: int) -> PresentsModel | None:
    order = session.scalar(select(PresentsModel).where(PresentsModel.id == present_id))
    return order


def update_present(present_id: int, updates: dict) -> bool:
    try:
        session.query(PresentsModel).filter(PresentsModel.id == present_id).update(updates)
        session.commit()
        bot_logger.info("present '" + str(present_id) + "' successfully updated!")
        return True
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            "Integrity error in update_present - can't commit in db", exc_info=e
        )
        return False

