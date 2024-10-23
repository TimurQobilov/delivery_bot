import telebot
import buttons as bt
from geopy import Photon


geolocator = Photon(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
bot = telebot.TeleBot(token="")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать в бот доставки!")
    bot.send_message(user_id, "Введите своё имя для регистрации")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    bot.send_message(user_id, f"Привет {name}!")
    bot.send_message(user_id, f"Теперь поделитесь своим номером, {name}", reply_markup=bt.phone_button())
    bot.register_next_step_handler(message, get_phone_number, name)

def get_phone_number(message, name):
    name = message.from_user.first_name
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text  # Если номер введен вручную
    bot.send_message(user_id, f"Отправьте свою локацию {name}", reply_markup=bt.location_button())
    bot.register_next_step_handler(message, get_location, name, phone_number)

def get_location(message, name, phone_number):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = geolocator.reverse((latitude, longitude)).address
        print(name, phone_number, address)
        bot.send_message(user_id, "Вы успешно зарегистрировались!")
        bot.send_message(user_id, "Главное меню:")
    else:
        bot.send_message(user_id, "Пожалуйста, отправьте свою локацию через кнопку")
        bot.register_next_step_handler(message, get_location, name, phone_number)

bot.infinity_polling()
