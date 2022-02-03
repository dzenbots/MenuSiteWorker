from peewee import Model

from loader import dp


class SqliteBaseModel(Model):
    class Meta:
        database = dp.bot['database']


def on_startup_sqlite():
    dp.bot['database'].connect()
    dp.bot['database'].create_tables([

    ], safe=True)


def on_shutdown_sqlite():
    dp.bot['database'].close()
