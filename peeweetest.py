from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime
import time
custom_db = SqliteExtDatabase('blah.db')
class BaseModel(Model):
    class Meta:
        database = custom_db


class User(BaseModel):
    name = CharField(unique=True)
    time = IntegerField()

custom_db.connect()
# custom_db.create_tables([User])

# db.connect()
try:
    charlie = User.create(name='charlie', time=0)
    charlie.save()
except:
    print "user creation error"
# User.create(name='benard').save()

try:
    print User.get(User.name == 'sally')
except DoesNotExist:
    print "Does not exist"

user = User.get(User.name == 'charlie')
user.time = int(time.time())
user.save()

print user.time

print User.get(User.name == 'charlie').time