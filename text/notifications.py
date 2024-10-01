from config import ONE_DAY_SALE, BUY_INSTR_URL


def new_user_notification_text():
    return (f"Если тебе нужна помощь по использованию бота, можешь воспользоваться <a href='{BUY_INSTR_URL}'>инструкцией</a>\n\n"
            "А чтобы уже сейчас начать пользоваться VPN, нажми кнопку <i>«Купить»</i>")


def sale_one_day_notification_text():
    return ("🔥 <i>ГОРЯЧЕЕ ПРЕДЛОЖЕНИЕ!</i>\n\n"
            "<b>Для новых пользователей действует акция - " + str(ONE_DAY_SALE) + "% на месячную подписку!</b>\n\n"
            "💸 Чтобы оформить ее нажми кнопку <i>«Купить»</i>\n\n"
            "<i>P.S скидка актуальна только в течение 24 часов</i>")