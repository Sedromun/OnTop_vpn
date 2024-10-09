from config import BOT_URL, REFS_PARAM

datetime_format = "%d-%m-%Y %H:%M"


def get_referral_link(user_id):
    return BOT_URL + REFS_PARAM + str(user_id)
