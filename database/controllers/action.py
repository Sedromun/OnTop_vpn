from sqlalchemy.exc import IntegrityError

from database import session
from logs import bot_logger
from schemas.action import ActionModel


def create_action(
    user_id: int,
    title: str,
    description: str,
) -> ActionModel | None:
    action = ActionModel(
        user_id=user_id,
        title=title,
        description=description,
    )

    session.add(action)

    try:
        session.commit()
        bot_logger.info(
            "action '" + str(action.id) + "' successfully added!"
        )
        return action
    except IntegrityError as e:
        session.rollback()
        bot_logger.exception(
            "Integrity error in create_action - can't commit in db", exc_info=e
        )
        return None