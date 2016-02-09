import sys
import time
import telepot
import settings

"""
$ python2.7 skeleton.py <token>
"""

def handle(msg):
    flavor = telepot.flavor(msg)

    # a normal message
    if flavor == 'normal':
        content_type, chat_type, chat_id = telepot.glance2(msg)
        print content_type, chat_type, chat_id

        # Do your stuff according to `content_type` ...

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