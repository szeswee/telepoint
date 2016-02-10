import sys
import telepot
from telepot.delegate import per_chat_id, call, create_open
import settings
# import models
from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import *

db = SqliteExtDatabase('telepoints.db')

magic = {}

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    chat_id = CharField(unique=True)
    state = CharField(default='/start')
    unixtimestamp = IntegerField(default=0)

db.connect()
# db.create_tables([User])

try:
    charlie = User.create(chat_id='98011962')
    charlie.save()
except:
    print "user creation error"