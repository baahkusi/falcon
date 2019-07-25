import datetime
from peewee import *
from .config import DB_NAME, DB_USER, DB_HOST, DB_PSWD

db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PSWD, host=DB_HOST)


class BaseModel(Model):

    utime = TimestampField()
    ctime = TimestampField()

    class Meta:
        database = db


class User(BaseModel):

    email = CharField(max_length=256, unique=True)
    level = SmallIntegerField(default=1)  # 1 - 4
    points = IntegerField(default=0)
    is_active = BooleanField(default=True)
    # client | staff | addmin | superuser | root
    user_type = CharField(max_length=256, default='client')


class Login(BaseModel):

    user = ForeignKeyField(User, backref='logins')
    pin = IntegerField(null=True)
    device = TextField(null=True)
    token = CharField(max_length=512, null=True)
    duration = SmallIntegerField(default=30, null=True)


class Language(BaseModel):

    name = CharField(max_length=256)
    description = TextField()


class Entry(BaseModel):

    entry = TextField()
    level = SmallIntegerField(default=1)  # -> 1 - 4
    language = ForeignKeyField(Language, backref='entries')
    is_translated = BooleanField(default=False)
    is_validated = BooleanField(default=False)


class Translation(BaseModel):

    entry = ForeignKeyField(Entry, backref="translations")
    translation = TextField()


class Validation(BaseModel):

    translation = ForeignKeyField(Translation, backref="validations")
    validation = BooleanField()


class PeeweeConnectionMiddleware(object):
    def process_request(self, req, resp):
        db.connect()

    def process_response(self, req, resp, resource, req_succeeded):
        if not db.is_closed():
            db.close()


if __name__ == "__main__":
    import sys

    def up():
        db.create_tables([
            User, Login, Language, Entry, Translation, Validation,
        ])

    def down():
        db.drop_tables([
            User, Login, Language, Entry, Translation, Validation,
        ])

    try:
        if sys.argv[1] == "+":
            up()
            print("Successfully created tables ...")
        elif sys.argv[1] == "-":
            down()
            print("Successfully dropped tables ...")
        elif sys.argv[1] == "-+":
            down()
            up()
            print("Successfully reloaded tables ...")
        else:
            print(f"Could not execute {sys.argv[1]}")
    except Exception as e:
        print(e)
