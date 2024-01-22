from peewee import SqliteDatabase, Model, PrimaryKeyField, BooleanField, CharField, ForeignKeyField, IntegerField

database = SqliteDatabase('../db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    username = CharField(primary_key=True, unique=True)
    full_name = CharField(null=True)
    chat_id = CharField()
    tracking = BooleanField(default=False)
    period = IntegerField(default=1)  # в минутах

    class Meta:
        db_table = 'users'
        order_by = 'username'


class Site(BaseModel):
    id = PrimaryKeyField(unique=True)
    url = CharField()
    user = ForeignKeyField(User, field='username', lazy_load=False, backref='sites')

    class Meta:
        db_table = 'sites'
        order_by = 'id'
