import telebot
import colarization

from telebot import types

OPENAI_API_KEY="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"
bot = telebot.TeleBot('6086389553:AAHT71kjpXRQBbC2e8oVCI6zLKZEQDB8ZUU')
chats = {}

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
    elif message.text == '/dialog' or message.text == 'Пообщаться с CHAT-GPT':
        send = bot.send_message(message.from_user.id, "Напишите сообщение, для прекращения общения напишите /stop")
        chats[message.from_user.id] = []
        bot.register_next_step_handler(send, dialog)
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')

def git(message):
    bot.send_message(message.from_user.id, 'https://github.com/DogNellaf/colorize-telegram-bot')

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Разукрасить картинку")
    button2 = types.KeyboardButton("Информация о разработчике")
    button3 = types.KeyboardButton("Репозиторий")
    button4 = types.KeyboardButton("Пообщаться с CHAT-GPT")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
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

def dialog(message):
    # Use the data from the CSV file to train or fine-tune GPT-3
    # (Assuming you have the OpenAI API key and the OpenAI Python library installed)

    if message.text == "/stop":
        bot.send_message(message.from_user.id, "Общение с CHAT-GPT остановлено")
        return

    chats[message.from_user.id].append({"role": "user",
                                        "content": message.text})

    if len(message.text) > 2049:
        bot.send_message(message.from_user.id, "Слишком длинное сообщнеие, отключаем CHAT-GPT")
        return

    import openai
    openai.api_key = OPENAI_API_KEY
    send = bot.send_message(message.from_user.id, "Ждем ответ...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chats[message.from_user.id]
    )
    print(response)

    chats[message.from_user.id].append({"role": "assistant",
                                     "content": response["choices"][0]["message"]["content"]})

    bot.send_message(message.from_user.id, response["choices"][0]["message"]["content"])
    bot.register_next_step_handler(send, dialog)

bot.polling(none_stop=True, interval=0)