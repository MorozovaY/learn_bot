import logging
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

today = '2021/09/10'
planet_dict = {
    'Mars': ephem.Mars(today),
    'Venus': ephem.Venus(today),
    'Saturn': ephem.Saturn(today),
    'Jupiter': ephem.Jupiter(today),
    'Neptune': ephem.Neptune(today),
    'Uranus': ephem.Uranus(today),
    'Mercury': ephem.Mercury(today)
    }

def greet_user(update, context):
    print ('Вызван /start')
    update.message.reply_text('Привет, друг!')

def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def which_constellation(update, context):
    planet_name = update.message.text.split()[1]
    ephem_body = planet_dict.get(planet_name, None)
    if ephem_body!=None:
        constellation = ephem.constellation(planet_dict[planet_name])
        update.message.reply_text(constellation[1])
    else:
        update.message.reply_text('Я не знаю такую планету!')

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler("planet", which_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info ('Bot started')
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()