from peewee import Model, TextField

from loader import dp


class SqliteBaseModel(Model):
    class Meta:
        database = dp.bot['database']


class SchoolStorageItem(SqliteBaseModel):
    name = TextField()
    hash = TextField()
    mime = TextField()
    parent_hash = TextField()


def on_startup_sqlite():
    dp.bot['database'].connect()
    dp.bot['database'].create_tables([
        SchoolStorageItem
    ], safe=True)
    SchoolStorageItem.get_or_create(
        name='files',
        hash=dp.bot.get('config').misc.school_auth.root_folder,
        mime='directory',
        parent_hash=dp.bot.get('config').misc.school_auth.root_folder
    )


def on_shutdown_sqlite():
    dp.bot['database'].close()
