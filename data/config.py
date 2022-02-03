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
class FilesConfig:
    tomorrow_folder_path: str
    today_folder_path: str
    local_dir_path: str
    local_dir_compressed_path: str
    mail_folder_name: str


@dataclass
class SchoolSiteAuth:
    base_addr: str
    login: str
    password: str
    root_folder: str


@dataclass
class SchedulerConfig:
    time_for_tomorrow: str
    time_for_today: str


@dataclass
class PyLovePDF_Keys:
    key1: str
    key2: str


@dataclass
class MailAuth:
    login: str
    password: str
    imap_server: str


@dataclass
class Miscellaneous:
    pdf_keys: PyLovePDF_Keys
    scheduler: SchedulerConfig
    school_auth: SchoolSiteAuth
    files_paths: FilesConfig
    mail_auth: MailAuth
    google_config: GoogleConfig = None


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
            files_paths=FilesConfig(
                tomorrow_folder_path=env.str("TOMORROW_MENU_FOLDER_PATH_IN_SITE_STORAGE"),
                today_folder_path=env.str("TODAY_MENU_FOLDER_PATH_IN_SITE_STORAGE"),
                local_dir_path=env.str("DIRECTORY_TO_SAVE_FILES"),
                local_dir_compressed_path=env.str("DIRECTORY_TO_SAVE_COMMPRESSED_FILES"),
                mail_folder_name=env.str("MENU_FOLDER_NAME_IN_MAIL_BOX"),
            ),
            pdf_keys=PyLovePDF_Keys(
                key1=env.str("PYLOVEPDF_API_KEY1"),
                key2=env.str("PYLOVEPDF_API_KEY2")
            ),
            scheduler=SchedulerConfig(
                time_for_tomorrow=env.str("TOMORROW_MENU_REPLACING_TIME"),
                time_for_today=env.str("TODAY_MENU_REPLACING_TIME")
            ),
            school_auth=SchoolSiteAuth(
                base_addr=env.str("BASE_SCHOOL_SITE_ADDR"),
                login=env.str("SITE_LOGIN"),
                password=env.str("SITE_PASSWORD"),
                root_folder=env.str("ROOT_FOLDER"),
            ),
            mail_auth=MailAuth(
                login=env.str("MAIL_LOGIN"),
                password=env.str("MAIL_PASSWORD"),
                imap_server=env.str("MAIL_IMAP_SERVER"),
            ),
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
