from spambot.templates.path import folder_path
from pydantic_settings import BaseSettings
from fastapi.templating import Jinja2Templates
import logging
from colorlog import ColoredFormatter


class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///database.db"
    db_echo: bool = True


templates = Jinja2Templates(directory=folder_path)
setting = Setting()

logger = logging.getLogger("logging")

# Устанавливаем уровень логирования (например, INFO)
logger.setLevel(logging.DEBUG)

# Создайте консольный обработчик
console_handler = logging.StreamHandler()

# Используйте ColoredFormatter для цветного форматирования
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

# Установите форматтер для обработчика
console_handler.setFormatter(formatter)

# Добавьте обработчик к логгеру
logger.addHandler(console_handler)
