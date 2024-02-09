import telebot
from telebot import types
from googletrans import Translator
# pip install googletrans==3.1.0a0
import localfiles


bot = telebot.TeleBot(localfiles.token)

@bot.message_handler(commands=["start"])
def func_one(self):
    markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("Вопросы", callback_data="callback_data"))
    bot.send_message(self.chat.id, f"Привет, <b>{self.from_user.first_name}</b>! Ответь на пару вопросов, чтобы я сгенерировал варианты твоей будущей профессий.\n\n<b>Инструкция:</b>\nПосле нажатия на кнопку, придёт сообщение, вам нужно ответить на все вопросы из него и отправить ответ <b>также</b> одним сообщением, оставляя ответы на впоросы на разных строчках. После бот обработает запрос и выдаст результат.\n\n<b>Рекомендации:</b>\n1. Использовать формальный язык и пишите развёрнутые ответы\n2. Следуйте теме профориентации\n3. Не пользуйтесь ненормативной лексикой\n<em>Чем больше напишешь, тем точнее будет результат</em>\n\n<em>В боте используется модель:</em> <b>GeminiProChat</b>", parse_mode="html", reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def func_two(self):
    if self.message:
        bot.send_message(self.message.chat.id, "* Какие виды деятельности и направления вас интересуют?\n* Какие критерии при выборе работы для вас важны?\n* В каком формате ты бы хотел работать?\n\nПример:\n<em>Меня интересует...\nДля меня важно...\nЯ бы хотел работать...</em>", parse_mode="html")

@bot.message_handler()
def func_three(self):
    message = bot.send_message(self.chat.id, "Пожалуйста, подождите немного, бот обрабатывает ваш запрос...")
    print(f'From ({self.from_user.username}): "{self.text}"')
    bot.edit_message_text(chat_id=self.chat.id, message_id=message.id, text=Translator().translate(localfiles.ask(localfiles.begin + Translator().translate(self.text, dest="en").text + localfiles.end), dest="ru").text.replace("*", ""))
    print(f'The message was successfully delivered to ({self.from_user.username})')

bot.infinity_polling()
