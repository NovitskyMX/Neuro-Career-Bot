import telebot
from googletrans import Translator
#Local imports:
from head import ask
from lToken import token

thematicWords = ["нравится", "увлекаюсь", "занимаюсь", "информатика", "математика", "программирование", "книги", "деньги", "оклад", "зарплата"]

bot = telebot.TeleBot(token)
translater = Translator()

# Commands:
@bot.message_handler(commands=["start"])
def fistMessage(x): # First message
    bot.send_message(x.chat.id, f"Привет, <b>{x.from_user.first_name}</b>! Ответь на пару вопросов, чтобы я сгенерировал варианты твоей будущей профессий.\n\n<b>Инструкция:</b>\nПосле нажатия на /questions придёт сообщение, вам нужно ответить на все вопросы из него и отправить ответ <b>также</b> одним сообщением, оставляя ответы на впоросы на разных строчках. После бот обработает запрос и выдаст результат.\n\n<b>Рекомендации:</b>\n1. Использовать формальный язык и пишите развёрнутые ответы\n2. Следуйте теме профориентации\n3. Не пользуйтесь ненормативной лексикой\n<em>Чем больше напишешь, тем точнее будет результат</em>\n\n<em>В боте используется модель:</em> <b>GeminiProChat</b>", parse_mode="html")

@bot.message_handler(commands=["questions"])
def message(x): # Questions
    bot.send_message(x.chat.id, "* Какие виды деятельности и направления вас интересуют?\n* Какие критерии при выборе работы для вас важны?\n* В каком формате ты бы хотел работать?")

@bot.message_handler()
def answer(x): # Message receiver
    bot.send_message(x.chat.id, "Пожалуйста, подождите немного, бот обрабатывает ваш запрос...")
    flag = False
    for i in x.text.lower().split():
        if i in thematicWords:
            flag = True
            break
    if flag:
        NeuroAsk = ask(translater.translate(x.text, dest="en").text + "\nMAKE A SELECTION of PROFESSIONS, describe the pros and cons for each of them, and also write which USE exams you need to take for each of the jobs.")
        res = translater.translate(NeuroAsk, dest="ru").text
        bot.send_message(x.chat.id, res)
    else:
        bot.send_message(x.chat.id, "Ваш запрос не прошел проверку, попробуйте снова.")

bot.infinity_polling() # Don't stop running