from peewee import SqliteDatabase, Model, PrimaryKeyField, BooleanField, CharField, ForeignKeyField, IntegerField
from src.settings import settings

database = SqliteDatabase(settings.DB_PATH)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    chat_id = CharField(primary_key=True, unique=True)
    username = CharField(null=True)
    full_name = CharField(null=True)
    tracking = BooleanField(default=False)
    period = IntegerField(default=1)  # в минутах

    class Meta:
        db_table = 'users'
        order_by = 'chat_id'


class Site(BaseModel):
    id = PrimaryKeyField(unique=True)
    url = CharField()
    user = ForeignKeyField(User, field='chat_id', lazy_load=False, backref='sites')

    class Meta:
        db_table = 'sites'
        order_by = 'id'
