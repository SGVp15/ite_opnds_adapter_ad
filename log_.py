import logging

from config import LOG_FILE

file_log = logging.FileHandler(LOG_FILE)
console_out = logging.StreamHandler()


def configure_logging(level=logging.INFO):
    logging.basicConfig(
        handlers=(file_log, console_out),
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
        # encoding='utf-8',
    )


log = logging.getLogger(__name__)
configure_logging()
