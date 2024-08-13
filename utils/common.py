from config import REFS_PARAM, BOT_LINK

datetime_format = "%d-%m-%Y %H:%M"


def get_referral_link(user_id):
    return BOT_LINK + REFS_PARAM + str(user_id)
