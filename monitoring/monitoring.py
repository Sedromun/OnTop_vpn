from database.controllers.user import get_referrals, get_user


def collect_user_info(user_id: int):
    user = get_user(user_id)
    referrals = get_referrals(user_id)

    orders = user.orders

    user_info = {
        "user_id": user_id,
        "balance": user.balance,
        "referrals": len(referrals),
    }
