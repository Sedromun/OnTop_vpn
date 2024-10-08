from config import ONE_DAY_SALE, INSTR_URL


def new_user_notification_text():
    return (
        f"Если тебе нужна помощь по использованию бота, можешь воспользоваться <a href='{INSTR_URL}'>инструкцией</a>\n\n"
        "А чтобы уже сейчас начать пользоваться VPN, нажми кнопку <i>«Купить»</i>")


def sale_one_day_notification_text():
    return ("🔥 <i>ГОРЯЧЕЕ ПРЕДЛОЖЕНИЕ!</i>\n\n"
            "<b>Для новых пользователей действует акция - " + str(ONE_DAY_SALE)
            + "% на месячную подписку!</b>\n\n"
              "💸 Чтобы оформить ее нажми кнопку <i>«Купить»</i>\n\n"
              "<i>P.S скидка актуальна только в течение 24 часов</i>")


def auto_extended_success(order_id):
    return f"Ключ {order_id} -  успешно продлен"


def auto_extended_failure(order_id):
    return (f"Автопродление для ключа {order_id} не сработало, продлите вручную по кнопке ниже\n"
            f"Продлили ключ на день")
