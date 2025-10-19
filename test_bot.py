import telebot
from telebot import types
import json

BOT_TOKEN = "6644637602:AAEVKKrYraoHa9Wm1augxMrWYSK8I8K-HEw"
BOOKING_URL = "https://yabuzuk.github.io/clinerkipr/booking.html"
ADMIN_ID = "407457753"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    web_app = types.WebAppInfo(url=BOOKING_URL)
    btn = types.InlineKeyboardButton("📅 Записаться", web_app=web_app)
    markup.add(btn)
    
    bot.send_message(message.chat.id, "Нажмите кнопку для записи:", reply_markup=markup)

@bot.message_handler(content_types=['web_app_data'])
def handle_data(message):
    print("=== ПОЛУЧЕНЫ ДАННЫЕ ===")
    print(f"От: {message.from_user.id}")
    print(f"Данные: {message.web_app_data.data}")
    
    bot.send_message(message.chat.id, "✅ Данные получены!")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Тестовый бот запущен...")
    bot.polling(none_stop=True)