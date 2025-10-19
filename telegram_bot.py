import telebot
from telebot import types
import json
from datetime import datetime

# Замените на ваш токен бота
BOT_TOKEN = "6644637602:AAEVKKrYraoHa9Wm1augxMrWYSK8I8K-HEw"
# URL вашей страницы записи
BOOKING_URL = "https://yabuzuk.github.io/clinerkipr/booking.html"
# ID канала для сохранения заявок (создайте приватный канал)
BOOKINGS_CHANNEL = "-1003161238645"
# ID администратора
ADMIN_ID = "407457753"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['myid'])
def get_my_id(message):
    bot.send_message(
        message.chat.id,
        f"Ваш Telegram ID: {message.from_user.id}"
    )

@bot.message_handler(commands=['test_channel'])
def test_channel(message):
    try:
        bot.send_message(BOOKINGS_CHANNEL, "🧪 Тест канала - бот работает!")
        bot.send_message(message.chat.id, "✅ Канал работает!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка канала: {e}")

@bot.message_handler(commands=['get_chat_id'])
def get_chat_id(message):
    bot.send_message(
        message.chat.id,
        f"ID этого чата: {message.chat.id}"
    )

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "🏓 Понг! Бот работает")
    print(f"Ping от пользователя {message.from_user.id}")

@bot.message_handler(commands=['test_send'])
def test_send(message):
    if str(message.from_user.id) != ADMIN_ID:
        return
    
    test_data = {
        'name': 'Тест',
        'phone': '89999999999',
        'date': '2025-10-20',
        'time': '10:00',
        'service': 'general',
        'area': '50',
        'address': 'Тестовый адрес',
        'notes': 'Тест'
    }
    
    booking_id = f"TEST{datetime.now().strftime('%H%M%S')}"
    
    channel_message = f"""
🆔 #{booking_id}
👤 {test_data['name']}
📞 {test_data['phone']}
📅 {test_data['date']} {test_data['time']}
🧹 {test_data['service']}
📐 {test_data['area']} м²
📍 {test_data['address']}
📝 {test_data['notes']}
⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}
🔄 Тест
"""
    
    try:
        result = bot.send_message(BOOKINGS_CHANNEL, channel_message)
        bot.send_message(message.chat.id, f"✅ Тест успешен! ID: {result.message_id}")
        print(f"Тестовое сообщение отправлено в канал")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")
        print(f"Ошибка отправки в канал: {e}")

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

@bot.message_handler(func=lambda message: True)
def debug_all_messages(message):
    print(f"Получено сообщение: {message.content_type} от {message.from_user.id}")
    if hasattr(message, 'web_app_data') and message.web_app_data:
        print(f"Web App Data: {message.web_app_data.data}")
    # Пропускаем обработку дальше

@bot.message_handler(content_types=['web_app_data'])
def handle_booking_data(message):
    print(f"=== ПОЛУЧЕНЫ ДАННЫЕ WEB APP ===")
    print(f"Пользователь: {message.from_user.id}")
    print(f"Сырые данные: {message.web_app_data.data}")
    data = json.loads(message.web_app_data.data)
    print(f"Обработанные данные: {data}")
    
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
    print(f"Попытка отправить в канал: {BOOKINGS_CHANNEL}")
    try:
        result = bot.send_message(BOOKINGS_CHANNEL, channel_message)
        print(f"Успешно отправлено в канал: {result.message_id}")
    except Exception as e:
        print(f"ОШИБКА отправки в канал: {e}")
    
    # Отправляем подтверждение клиенту
    try:
        bot.send_message(
            message.chat.id,
            f"✅ Заявка #{booking_id} принята!\n"
            "Мы свяжемся с вами для подтверждения."
        )
        print(f"Подтверждение отправлено клиенту")
    except Exception as e:
        print(f"Ошибка отправки клиенту: {e}")
    
    print("=== ОБРАБОТКА ЗАВЕРШЕНА ===")

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
    # Удаляем webhook если он активен
    bot.remove_webhook()
    print("Бот запущен...")
    bot.polling(none_stop=True)