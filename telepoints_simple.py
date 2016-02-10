import sys
import telepot
from telepot.delegate import per_chat_id, call, create_open
import settings, lang_dict
# import models
from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import *
import time, datetime, re
"""
telepoints.py
"""

db = SqliteExtDatabase('telepoints.db')

magic = {}
lang = {"key":"normal"}

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    chat_id = CharField(unique=True)
    state = CharField(default='/start')
    unixtimestamp = IntegerField(default=0)


def is_proper_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y')
        return True
    except ValueError:
        return False

def is_proper_datetime(date_text):
    # 08/12/2016
    try:
        datetime.datetime.strptime(date_text, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        return False


def message_manager(msg, chat_id, state):
    # user must exist
    text = msg['text']
    keyboard = {'hide_keyboard': True}
    user = User.get(User.chat_id == chat_id)

    if text == '/cancel':
        user.state = '/start'
        user.save()
        bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["cancel"], reply_markup=keyboard)
    elif text == '/language':
        bot.sendMessage(chat_id, "Select a language with \"/lanuage normal/rude/allcaps/narrator.\"")
    elif text == '/language normal':
        lang["key"] = "normal"
    elif text == '/language narrator':
        lang["key"] = "narrator"
    elif text == '/language allcaps':
        lang["key"] = "allcaps"
    elif text == '/language rude':
        lang["key"] = "rude"
    elif state == '/start':
        if text == '/start':
            # customer or service provider
            keyboard = {'keyboard': [['/customer'], ['/provider']]}
            bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["start"], reply_markup=keyboard)
        elif text == '/customer':
            # process customer
            keyboard = {'keyboard': [['/make'], ['/change']]}
            bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["customer"], reply_markup=keyboard)
            user.state = '/customer'
            user.save()
        elif text == '/provider':
            keyboard = {'keyboard': [['/week']]}
            bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["provider"], reply_markup=keyboard)
            user.state = '/provider'
            user.save()
        else:
            pass
    elif state == '/customer':
        if text == '/make':
            keyboard = {'keyboard': [['19/9/2016 09:00'], ['20/9/2016 11:00'], ['21/9/2016 15:30'], ['Choose my own']]}
            magic[chat_id] = [['19/9/2016 09:00'], ['20/9/2016 11:00'], ['21/9/2016 15:30'], ['Choose my own']]
            bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["make"], reply_markup=keyboard)
            user.state = '/make'
            user.save()
        elif text == "/change":
            keyboard = {'keyboard': [['19/9/2016 09:00'], ['20/9/2016 11:00'], ['21/9/2016 15:30'], ['Choose my own']]}
            magic[chat_id] = [['19/9/2016 09:00'], ['20/9/2016 11:00'], ['21/9/2016 15:30'], ['Choose my own']]
            bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["change"], reply_markup=keyboard)
            user.state = '/change'
            user.save()
        else:
            bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["nocmd"])

    elif state == '/make':
        # elif text matches date time format then do stuff
        # if text is choose my own, send the date format
        if text == 'Choose my own':
            bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["customdate"], reply_markup=keyboard)
            user.state = '/makecustom'
            user.save()
        elif is_proper_datetime(text):
            keyboard = {'keyboard': [magic[chat_id]]}
            bot.sendMessage(chat_id, "Booked! Waiting for approval!", reply_markup=keyboard)
        else:
            print magic
            pass

    elif state == '/makecustom':
        # if date format
        #   show list of timings
        # elif is single number submit request

        if is_proper_date(text):
            # get list which can be up to 16 options : shoul dbe list of options 1-16?
            # tell how to choose or select another date
            keyboard = {'keyboard': [magic[chat_id]]}
            bot.sendMessage(chat_id, "Choose a number and respond with 1 to 16.", reply_markup=keyboard)
        elif re.match('(^[1-9]$)|(^1[0-6]$)', text):
            # is a num between 1 and 16 (inclusive)
            print "Option " + text + " chosen"
            pass
        else:
            # bot.sendMessage(chat_id, "Specify dd/mm/yyyy or choose an option if it has been presented", reply_markup=keyboard)
            bot.sendMessage(chat_id, lang_dict.obj[lang["key"]]["nocmd"])
            pass


    elif state == '/change':
        # query for existing appointments
        # if exists continue
            # if text matches date time format then do stuff
            # elif text is choose my own do something
        # else go back to /start : please book something first
        pass

    elif state == '/changecustom':
        # if date format
        #   show list of timings
        # elif is single number submit request
        pass

    elif state == '/provider':
        if text == '/week':
            # show cal
            pass
        else:
            pass
    else:
        bot.sendMessage(chat_id, "Unrecognized input! ):", reply_markup=keyboard)


def is_active_user(user):
    # check if last message was >= 20s
    # as a measure of 'activeness'
    print "check active user"
    if (int(time.time()) - user.unixtimestamp) <= 20:
        return True
    return False

def is_base_state(user):
    if user.state == '/start':
        return True
    return False

class MsgHandler(telepot.helper.UserHandler):
    def __init__(self, seed_tuple, timeout):
        super(MsgHandler, self).__init__(seed_tuple, timeout, flavors=['normal'])

    def on_message(self, msg):
        """
        Preliminary processing of messages
        """
        flavor = telepot.flavor(msg)
        if flavor == 'normal':
            content_type, chat_type, chat_id = telepot.glance2(msg)
            print content_type, chat_type, chat_id

            # try to get user object
            user = None
            try:
                user = User.get(User.chat_id == chat_id)
            except DoesNotExist:
                pass

            # actual stuff
            if user is not None:
                if is_active_user(user):
                    user.unixtimestamp = int(time.time())
                    user.save()
                    message_manager(msg, chat_id, user.state)
                else:
                    # expired session, restart
                    print "expired"
                    msg['text'] = '/start'
                    user = User.get(User.chat_id == chat_id)
                    user.unixtimestamp = int(time.time())
                    user.state = '/start'
                    user.save()
                    message_manager(msg, chat_id, user.state)

            elif user is None:
                # register
                print "not registered"
                pass
            else:
                bot.sendMessage(chat_id, "Oops. Something happened.")

"""
Bot initialisation happens here
"""
TOKEN = settings.TOKEN # get token from settings file

bot = telepot.DelegatorBot(TOKEN, [
    # timeout if nothing after 20s
    (per_chat_id(), create_open(MsgHandler, timeout=20)),
])

# bot.sendMessage("98011962", "Unrecognized input! ):")

bot.notifyOnMessage(run_forever=True)