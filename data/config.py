from dataclasses import dataclass
from typing import Any, Union

from environs import Env
from google.oauth2.service_account import Credentials


@dataclass
class SqliteConfig:
    filename: str


@dataclass
class PostgresConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class GoogleConfig:
    google_scoped_credentials: Any = None
    google_spreadsheet_key: str = None


@dataclass
class Miscellaneous:
    google_config: GoogleConfig = None
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous
    db: Union[PostgresConfig, SqliteConfig, None] = None


def get_scoped_credentials(credentials, scopes):
    def prepare_credentials():
        return credentials.with_scopes(scopes)

    return prepare_credentials


def load_config(path: str = None):
    env = Env()
    env.read_env(path)
    use_google = env.bool('USE_GOOGLE')

    use_database = env.bool("USE_DATABASE")
    db_type = env.str("DB_TYPE")

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=None if not use_database else
        PostgresConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ) if db_type == "POSTRESQL" else
        SqliteConfig(
            filename=env.str("SQLITE_DB_FILENAME")
        ) if db_type == "SQLITE" else None,
        misc=Miscellaneous(
            google_config=GoogleConfig(
                google_scoped_credentials=get_scoped_credentials(
                    credentials=Credentials.from_service_account_file(env.str('GOOGLE_CREDENTIALS_FILE')),
                    scopes=[
                        "https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                        "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"
                    ]
                ),
                google_spreadsheet_key=env.str('GOOGLE_SPREADSHEET_KEY')
            ) if use_google else None
        )
    )
