from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///database.db"
    db_echo: bool = True


setting = Setting()
