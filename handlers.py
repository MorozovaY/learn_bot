import ephem
from glob import glob
from random import randint, choice

from utils import get_smile, main_keyboard, play_random_numbers

def greet_user(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!", reply_markup=main_keyboard())

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    update.message.reply_text(f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}", reply_markup=main_keyboard())

def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"
    update.message.reply_text(message, reply_markup=main_keyboard())

def send_cat_picture(update, context):
    cat_photos_list = glob('images/cat*.jp*g')
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, 'rb'), reply_markup=main_keyboard())

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )

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

def which_constellation(update, context):
    planet_name = update.message.text.split()[1]
    ephem_body = planet_dict.get(planet_name, None)
    if ephem_body!=None:
        constellation = ephem.constellation(planet_dict[planet_name])
        update.message.reply_text(constellation[1])
    else:
        update.message.reply_text('Я не знаю такую планету!')