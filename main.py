import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# Запуск фонового веб-сервера для Render
threading.Thread(target=run_health_check, daemon=True).start()

import telebot
from telebot import types

# Твій токен від BotFather
BOT_TOKEN = "8693227554:AAFRGDTzkepMq1sDeAEqXxBz_7sEKcdTvfw"

bot = telebot.TeleBot(BOT_TOKEN)

# 1. Обробка команди /start
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    
    # Створюємо кнопку "Я человек ✅"
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        text="Я человек ✅", 
        callback_data=f"verify_{user_id}"
    )
    keyboard.add(button)

    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Для получения ссылки на канал подтверди, что ты не бот.",
        reply_markup=keyboard
    )

# 2. Обробка натискання на кнопку "Я человек ✅"
@bot.callback_query_handler(func=lambda call: call.data.startswith('verify_'))
def process_verify(call):
    user_id = int(call.data.split("_")[1])

    # Перевірка, чи це той самий користувач натискає
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, "Эта кнопка не для тебя!", show_alert=True)
        return

    # Твоє приватне посилання на канал
    CHANNEL_LINK = "https://t.me/+pLsmj3DY-UQyOGEx" 

    # Змінюємо текст повідомлення після натискання кнопки
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ Проверка пройдена! Держи ссылку на канал:\n{CHANNEL_LINK}"
    )
    bot.answer_callback_query(call.id)

# 3. Реагувати на будь-яке інше текстове повідомлення
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    start_cmd(message)

if __name__ == '__main__':
    
    print("Бот запущен...")
    bot.infinity_polling()
