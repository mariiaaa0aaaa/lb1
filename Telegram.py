from telethon import TelegramClient
import asyncio

api_id = '29674717'  # ваш API ID
api_hash = '2bc47165f9f210cf6be0829fd7cde485'  # ваш API Hash
bot_token = '7245603063:AAGZ-x-q8eMzbTZgcVR0jVJ7QaTH8EXe88c'  # токен вашого бота
group_id = 2422066186  # ID вашої групи
message_to_send = 'Сообщение отправилось в чат.'  # повідомлення, яке ви хочете надіслати


async def main():
    client = TelegramClient('my_bot', api_id, api_hash)
    await client.start(bot_token=bot_token)

    try:
        # отримання учасників групи
        participants = await client.get_participants(group_id)

        if participants:
            # вивід всіх учасників з нумерацією
            print("Список учасників:")
            for index, user in enumerate(participants, start=1):  # Нумерація починається з 1
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