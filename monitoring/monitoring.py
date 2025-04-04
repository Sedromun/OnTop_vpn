from database.controllers.user import get_referrals, get_user
from schemas import OrderModel


def collect_orders_info(orders: [OrderModel]):
    return [{
        'price': order.price,
        'country': order.country,
        'is_auto_on': order.payment_id is not None and order.payment_id != '',
        'begin_date': str(order.begin_date),
        'expiration_date': str(order.expiration_date)
    } for order in orders]


def collect_user_actions(actions):
    return [{
        'time': str(action.date_time),
        'title': action.title,
        'description': action.description,
    } for action in actions]


def collect_user_info(user_id: int):
    user = get_user(user_id)
    referrals = get_referrals(user_id)

    orders = user.orders
    active_orders_info = collect_orders_info(orders)
    finished_orders = user.finished_orders
    finished_orders_info = collect_orders_info(finished_orders)

    actions = user.actions
    actions_info = collect_user_actions(actions)

    return {
        "user_id": user_id,
        "balance": user.balance,
        "created_time": str(user.created_time),
        "referrals": len(referrals),
        "orders": active_orders_info,
        "finished_orders": finished_orders_info,
        "actions": actions_info,
        "review": user.review
    }
