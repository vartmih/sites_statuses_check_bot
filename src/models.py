from peewee import SqliteDatabase, Model, PrimaryKeyField, BooleanField, CharField, ForeignKeyField

database = SqliteDatabase('../db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = database
        order_by = 'id'


class User(BaseModel):
    username = CharField(primary_key=True, unique=True)
    full_name = CharField(null=True)
    chat_id = CharField()
    tracking = BooleanField(default=False)

    class Meta:
        db_table = 'users'


class Site(BaseModel):
    id = PrimaryKeyField(unique=True)
    url = CharField()
    user = ForeignKeyField(User, field='username', lazy_load=False, backref='sites')

    class Meta:
        db_table = 'sites'
