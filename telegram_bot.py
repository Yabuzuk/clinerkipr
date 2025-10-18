import telebot
from telebot import types
import json
from datetime import datetime

# Замените на ваш токен бота
BOT_TOKEN = "YOUR_BOT_TOKEN"
# URL вашей страницы записи
BOOKING_URL = "https://yourdomain.com/booking.html"
# ID канала для сохранения заявок (создайте приватный канал)
BOOKINGS_CHANNEL = "@your_bookings_channel"
# ID администратора
ADMIN_ID = "YOUR_ADMIN_ID"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    
    # Создаем кнопку Web App для записи
    web_app = types.WebAppInfo(url=BOOKING_URL)
    booking_btn = types.InlineKeyboardButton(
        text="📅 Записаться на клининг", 
        web_app=web_app
    )
    markup.add(booking_btn)
    
    bot.send_message(
        message.chat.id,
        "🧹 Добро пожаловать в клининговую компанию!\n\n"
        "Нажмите кнопку ниже для записи на услуги клининга.\n"
        "Ваши данные будут автоматически заполнены.",
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_booking_data(message):
    data = json.loads(message.web_app_data.data)
    
    # Генерируем ID заявки
    booking_id = f"B{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Форматируем сообщение для канала (база данных)
    channel_message = f"""
🆔 #{booking_id}
👤 {data.get('name', 'Не указано')}
📞 {data.get('phone', 'Не указан')}
📅 {data.get('date', 'Не указана')} {data.get('time', 'Не указано')}
🧹 {data.get('service', 'Не указана')}
📐 {data.get('area', 'Не указана')} м²
📍 {data.get('address', 'Не указан')}
📝 {data.get('notes', 'Нет')}
⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}
🔄 Новая
"""
    
    # Сохраняем в канал
    try:
        bot.send_message(BOOKINGS_CHANNEL, channel_message)
    except Exception as e:
        print(f"Ошибка сохранения в канал: {e}")
    
    # Отправляем подтверждение клиенту
    bot.send_message(
        message.chat.id,
        f"✅ Заявка #{booking_id} принята!\n"
        "Мы свяжемся с вами для подтверждения."
    )

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if str(message.from_user.id) != ADMIN_ID:
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📋 Все заявки", callback_data="view_all"))
    markup.add(types.InlineKeyboardButton("🔍 Поиск по дате", callback_data="search_date"))
    markup.add(types.InlineKeyboardButton("📊 Статистика", callback_data="stats"))
    
    bot.send_message(
        message.chat.id,
        "🔧 Админ панель:\n\nВыберите действие:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_admin_callbacks(call):
    if str(call.from_user.id) != ADMIN_ID:
        return
    
    if call.data == "view_all":
        bot.send_message(
            call.message.chat.id,
            "📋 Все заявки сохранены в канале:\n" + BOOKINGS_CHANNEL
        )
    elif call.data == "search_date":
        bot.send_message(
            call.message.chat.id,
            "🔍 Для поиска по дате используйте поиск в канале:\n" + BOOKINGS_CHANNEL
        )
    elif call.data == "stats":
        bot.send_message(
            call.message.chat.id,
            "📊 Статистика доступна через просмотр канала:\n" + BOOKINGS_CHANNEL
        )

# Команды для управления заявками
@bot.message_handler(commands=['update_status'])
def update_booking_status(message):
    if str(message.from_user.id) != ADMIN_ID:
        return
    
    # Формат: /update_status B20241201120000 Подтверждена
    try:
        parts = message.text.split(' ', 2)
        booking_id = parts[1]
        new_status = parts[2]
        
        bot.send_message(
            message.chat.id,
            f"✅ Статус заявки #{booking_id} обновлен на: {new_status}\n\n"
            f"Обновите статус в канале {BOOKINGS_CHANNEL} вручную."
        )
    except:
        bot.send_message(
            message.chat.id,
            "❌ Неверный формат. Используйте:\n"
            "/update_status B20241201120000 Подтверждена"
        )

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)