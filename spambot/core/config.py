from pydantic_settings import BaseSettings
from fastapi.templating import Jinja2Templates


class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///database.db"
    db_echo: bool = True


templates = Jinja2Templates(directory="C:\\PythonPrograms\\SpamBot\\spambot\\templates")
setting = Setting()
