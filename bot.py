import telebot
import colarization

from telebot import types

bot = telebot.TeleBot('6086389553:AAHT71kjpXRQBbC2e8oVCI6zLKZEQDB8ZUU')
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start' or message.text == '/help':
        menu(message)
    elif message.text == '/info' or message.text == 'Информация о разработчике':
        info(message)
    elif message.text == '/colorize' or message.text == 'Разукрасить картинку':
        send = bot.send_message(message.from_user.id, "Пришлите фото")
        bot.register_next_step_handler(send, colorize)
    elif message.text == '/git' or message.text == 'Репозиторий':
        git(message)
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')

def git(message):
    bot.send_message(message.from_user.id, 'https://github.com/DogNellaf/colorize-telegram-bot')

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Разукрасить картинку")
    button2 = types.KeyboardButton("Информация о разработчике")
    button3 = types.KeyboardButton("Репозиторий")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, "Меню".format(message.from_user), reply_markup=markup)

def colorize(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(f"{file_id}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.send_message(message.from_user.id, "Фото получено, обрабатываю....")
        colarization.colorize(f"{file_id}.jpg")
        bot.send_photo(message.chat.id, open(f"{file_id}.jpg", 'rb'))
    except:
        bot.send_message(message.from_user.id, "Выберите новую команду еще раз")

def info(message):
    bot.send_message(message.from_user.id, "Разработал Сидоров Данил Михайлович, студент группы 1мБД2 в 2023 году")

bot.polling(none_stop=True, interval=0)