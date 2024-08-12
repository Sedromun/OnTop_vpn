import logging
import traceback

logging.basicConfig(
    level=logging.INFO,
    filename=".logs/bot_log.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
)


class Logger:
    @staticmethod
    def info(msg):
        logging.info(msg=msg)

    @staticmethod
    def exception(exc: Exception, msg: str | None = None):
        logging.exception(
            msg="Failed with Exception, short msg: {str(exc)}\n"
            + (f"custom message: \n{msg}\n" if msg is not None else "")
            + f"stack trace: \n"
            + "".join(traceback.TracebackException.from_exception(exc=exc).format())
        )

    @staticmethod
    def warning(msg: str | None = None):
        logging.warning(msg="Warning: " + msg)
