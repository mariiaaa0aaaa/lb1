import os
import asyncio
from telethon import TelegramClient

# запит у користувача API ID, API Hash, токен бота та ID групи в командному
api_id = input("Введіть ваш API ID: ")
api_hash = input("Введіть ваш API Hash: ")
bot_token = input("Введіть токен вашого бота: ")
group_id = int(input("Введіть ID вашої групи: "))
message_to_send = 'Сообщение отправилось в чат.'  # повідомлення, яке надсилається

async def main():
    client = TelegramClient('my_bot', api_id, api_hash)
    await client.start(bot_token=bot_token)

    try:
        # отримання учасників групи
        participants = await client.get_participants(group_id)

        if participants:
            # вивід всіх учасників з нумерацією
            print("Список учасників:")
            for index, user in enumerate(participants, start=1):
                print(f"{index}. {user.first_name} - {user.id}")
        else:
            print("У групі немає учасників або не вдалося отримати список учасників.")

        # відправка повідомлення в групу
        result = await client.send_message(group_id, message_to_send)

        # вивід тексту надісланого повідомлення без кавичок
        print(f"Повідомлення надіслано до групи з ID {group_id}: {result.message}")

    except Exception as e:
        print(f'Сталася помилка: {e}')

# запуск асинхронної функції
asyncio.run(main())