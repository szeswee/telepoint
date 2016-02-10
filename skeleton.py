import sys
import time
import telepot
import settings

"""
$ python2.7 skeleton.py <token>
"""

def message_manager(msg, chat_id):
     text = msg['text']
     keyboard = {'hide_keyboard': True}
     if text.startswith('/'):
         if text == '/start':
             # customer or service provider
             keyboard = {'keyboard': [['/customer'], ['/provider']]}
             bot.sendMessage(chat_id, "Customer or provider? CAKE OR DEATH???", reply_markup=keyboard)
         elif text == '/customer':
             keyboard = {'keyboard': [['/make'], ['/change'], ['cancel']]}
             bot.sendMessage(chat_id, "Ready to make an appointment?", reply_markup=keyboard)
         elif text == '/provider':
             keyboard = {'keyboard': [['/week']]}
             bot.sendMessage(chat_id, "Open the schedule for this week?", reply_markup=keyboard)
         elif text == '/help':
             bot.sendMessage(chat_id, "No can do.", reply_markup=keyboard)
         elif text == '/make':
             keyboard = {'keyboard': [['19/9/2016'], ['20/9/2016'], ['21/9/2016'], ['Choose my own']]}
             bot.sendMessage(chat_id, "Making hamrolls for everyone!", reply_markup=keyboard)
         elif text == '/change':
             keyboard = {'keyboard': [['20/9/2016']]}
             bot.sendMessage(chat_id, "Which appointment would you like to change?", reply_markup=keyboard)
         elif text == '/cancel':
             keyboard = {'keyboard': [['20/9/2016']]}
             bot.sendMessage(chat_id, "Like you have anything better to do that day.", reply_markup=keyboard)
         else:
             bot.sendMessage(chat_id, "Stop fucking shit up with your fat fingers!", reply_markup=keyboard)

def handle(msg):
    flavor = telepot.flavor(msg)
    print msg

    # a normal message
    if flavor == 'normal':
        content_type, chat_type, chat_id = telepot.glance2(msg)
        print content_type, chat_type, chat_id
        # bot.sendMessage(chat_id, msg['text'])
        # Do your stuff according to `content_type` ...
        if content_type == "text" and chat_type == "private":
             message_manager(msg, chat_id)
         else:
             bot.sendMessage(chat_id, "Message not understood. Do you need help? Type /help.")

    # an inline query - only AFTER `/setinline` has been done for the bot.
    elif flavor == 'inline_query':
        query_id, from_id, query_string = telepot.glance2(msg, flavor=flavor)
        print 'Inline Query:', query_id, from_id, query_string

        # Compose your own answers
        articles = [{'type': 'article',
                        'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

        bot.answerInlineQuery(query_id, articles)

    # a chosen inline result - only AFTER `/setinlinefeedback` has been done for the bot.
    elif flavor == 'chosen_inline_result':
        result_id, from_id, query_string = telepot.glance2(msg, flavor=flavor)
        print 'Chosen Inline Result:', result_id, from_id, query_string

        # Remember the chosen answer to do better next time

    else:
        raise telepot.BadFlavor(msg)

# TOKEN = sys.argv[1]  # get token from command-line
TOKEN = settings.TOKEN # get token from settings file

bot = telepot.Bot(TOKEN)
bot.notifyOnMessage(handle)
print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)