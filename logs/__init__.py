import datetime
import logging
import traceback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f".logs/{datetime.datetime.now().strftime('%Y_%m_%d')}_root_log.log",
)

bot_logger = logging.getLogger("bot")
checker_logger = logging.getLogger("checker")
backend_logger = logging.getLogger("backend")

bot_fh = logging.FileHandler(
    f".logs/{datetime.datetime.now().strftime('%Y_%m_%d')}_bot_log.log"
)
bot_fh.setLevel(logging.INFO)

checker_fh = logging.FileHandler(
    f".logs/{datetime.datetime.now().strftime('%Y_%m_%d')}_checker_log.log"
)
checker_fh.setLevel(logging.INFO)

backend_fh = logging.FileHandler(
    f".logs/{datetime.datetime.now().strftime('%Y_%m_%d')}_backend_log.log"
)
backend_fh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

bot_fh.setFormatter(formatter)
checker_fh.setFormatter(formatter)
backend_fh.setFormatter(formatter)

bot_logger.addHandler(bot_fh)
checker_logger.addHandler(checker_fh)
backend_logger.addHandler(backend_fh)


# class Logger:
#     @staticmethod
#     def info(msg):
#         logging.info(msg=msg)
#
#     @staticmethod
#     def exception(exc: Exception, msg: str | None = None):
#         logging.exception(
#             msg="Failed with Exception, short msg: {str(exc)}\n"
#             + (f"custom message: \n{msg}\n" if msg is not None else "")
#             + f"stack trace: \n"
#             + "".join(traceback.TracebackException.from_exception(exc=exc).format())
#         )
#
#     @staticmethod
#     def warning(msg: str | None = None):
#         logging.warning(msg="Warning: " + msg)
