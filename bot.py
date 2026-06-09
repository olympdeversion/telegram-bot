import asyncio
import sys
from telethon import TelegramClient, events

API_ID = 36295214 #   Ваш api_id с my.telegram.org
API_HASH = '9abc95279104bc3061654b082fbc1eaa'   # Ваш api_hash
PHONE_NUMBER = '+79331960493'   # Номер вашего аккаунта

client = TelegramClient('session_name', API_ID, API_HASH)

async def countdown(seconds):
    """Обратный отсчёт"""
    for remaining in range(seconds, 0, -1):
        minutes = remaining // 60
        secs = remaining % 60
        sys.stdout.write(f"\r⏱️ Следующая отправка через: {minutes:02d}:{secs:02d}")
        sys.stdout.flush()
        await asyncio.sleep(1)
    print("\r" + " " * 50 + "\r", end='')

async def main():
    await client.start(PHONE_NUMBER)
    print("✅ Бот запущен")
    
    # Выбор чата
    print("\n📋 Загрузка списка чатов...")
    dialogs = await client.get_dialogs()
    
    print("\n🔍 Доступные чаты:")
    chats = []
    count = 1
    for dialog in dialogs:
        if dialog.is_group or dialog.is_channel:
            print(f"{count}. {dialog.name}")
            chats.append(dialog.entity)
            count += 1
    
    choice = int(input("\n➡️ Введите номер чата: ")) - 1
    entity = chats[choice]
    print(f"✅ Выбран чат: {entity.title if hasattr(entity, 'title') else entity.first_name}")
    
    # 🆕 Запоминаем последнее отправленное сообщение
    last_message = None
    
    # 🆕 Обработчик ответов от ЛЮБОГО бота (на наши сообщения)
    @client.on(events.NewMessage)
    async def handle_reply(event):
        nonlocal last_message
        
        # Проверяем, что это ответ на наше сообщение
        if last_message and event.message.reply_to_msg_id == last_message.id:
            print(f"\n📩 Получен ответ на 'фиш'")
            
            # Проверяем, есть ли кнопки
            if event.message.buttons:
                print(f"🔘 Обнаружены кнопки! Нажимаю...")
                
                # Нажимаем все кнопки, которые есть
                for row in event.message.buttons:
                    for button in row:
                        print(f"   Нажимаю кнопку: {button.text}")
                        try:
                            # Пытаемся нажать через клик
                            await button.click()
                            print(f"   ✅ Кнопка нажата!")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print(f"   ❌ Ошибка при нажатии: {e}")
            else:
                print(f"📝 Ответ без кнопок: {event.message.text[:100]}")
    
    # Отправляем первое сообщение
    last_message = await client.send_message(entity, "фиш")
    print("\n🟢 Отправлено: фиш (первый раз)")
    
    # Основной цикл
    while True:
        await countdown(301)  # 5	 минут
        
        # Отправляем новое сообщение и запоминаем его
        last_message = await client.send_message(entity, "фиш")
        print("✅ Отправлено: фиш")

with client:
    client.loop.run_until_complete(main())