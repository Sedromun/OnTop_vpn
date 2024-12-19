# import datetime
#
# from fastapi import APIRouter
# from pydantic import BaseModel
#
# from config import w3, CONTRACT, TECH_SUPPORT_ADMIN
# from database.controllers.order import create_order
# from utils.payment import get_order_vless_key
#
# connection_router = APIRouter()
#
# # URL для API-методов
# SEND_TRANSACTION_URL = "/api/send_transaction"
# CHECK_NFT_URL = "/api/check_nft"
#
#
# class PaymentSchema(BaseModel):
#     amount: str
#
#
# @connection_router.post("/web3/pay_money")
# async def pay_money_handler(
#         payment_schema: PaymentSchema
# ):
#     payment = CONTRACT.functions.pay(payment_schema.amount).call()
#     begin = datetime.datetime.now(datetime.timezone.utc)
#     end = begin + datetime.timedelta(days=int(3))
#     order = create_order(
#         {
#             "user_id": TECH_SUPPORT_ADMIN,
#             "begin_date": begin,
#             "expiration_date": end,
#             "price": int(payment_schema.amount),
#         }
#     )
#     key = get_order_vless_key(order.id)
#     return {"key": key}
