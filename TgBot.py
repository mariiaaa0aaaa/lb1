import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Глобальні змінні для відстеження режиму "scream" і стану бота
screaming = False
bot_active = True  # Флаг для перевірки, чи активний бот

# Текст для меню
FIRST_MENU = "<b>Меню 1</b>\n\nОберіть режим."
SECOND_MENU = "<b>Меню 2</b>\n\nДодаткові параметри."

# Текст для кнопок
NEXT_BUTTON = "Далі"
BACK_BUTTON = "Назад"
LOUD_BUTTON = "Увімкнути режим капсу"
SILENT_BUTTON = "Вимкнути режим капсу"
STOP_BUTTON = "Зупинити бота"
START_BUTTON = "Запустити бота"
DOC_BUTTON = "Документ з результатами (скріншотами) кожного завдання 1ЛБ"

# Створення клавіатур для меню
FIRST_MENU_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)],
    [InlineKeyboardButton(LOUD_BUTTON, callback_data=LOUD_BUTTON)],
    [InlineKeyboardButton(SILENT_BUTTON, callback_data=SILENT_BUTTON)],
    [InlineKeyboardButton(STOP_BUTTON, callback_data=STOP_BUTTON)],
    [InlineKeyboardButton(START_BUTTON, callback_data=START_BUTTON)]
])
SECOND_MENU_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON)],
    [InlineKeyboardButton(DOC_BUTTON, url="https://docs.google.com/document/d/1t7fe5mNEcamnRK2Dwt321VHrEY-4Cmi1S4fi0hzTqc4/edit")],
])

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Функція для обробки текстових повідомлень."""
    if not bot_active:  # Якщо бот неактивний, нічого не робимо
        return

    print(f'{update.message.from_user.first_name} wrote {update.message.text}')
    if screaming and update.message.text:
        await context.bot.send_message(
            chat_id=update.message.chat.id,
            text=update.message.text.upper(),  # Перетворює текст на великі літери
            entities=update.message.entities
        )
    elif not screaming and update.message.text:
        await context.bot.send_message(
            chat_id=update.message.chat.id,
            text=update.message.text.lower(),  # Перетворює текст на маленькі літери
            entities=update.message.entities
        )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Відправка меню з кнопками в групу або приватний чат."""
    await context.bot.send_message(
        chat_id=update.message.chat.id,  # chat.id замість from_user.id
        text=FIRST_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=FIRST_MENU_MARKUP
    )

async def button_tap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обробка натискань кнопок в меню."""
    query = update.callback_query
    data = query.data

    global screaming, bot_active
    if data == LOUD_BUTTON:
        screaming = True
        await query.answer("Режим капсу увімкнено!")
    elif data == SILENT_BUTTON:
        screaming = False
        await query.answer("Режим капсу вимкнено!")
    elif data == STOP_BUTTON:
        bot_active = False  # Вимикаємо обробку повідомлень
        await query.answer("Бот зупиняється...")
        await context.bot.send_message(chat_id=query.message.chat.id, text="Бот зупинений.")
    elif data == START_BUTTON:
        bot_active = True  # Увімкнення обробки повідомлень
        await query.answer("Бот запущено!")
        await context.bot.send_message(chat_id=query.message.chat.id, text="Бот знову активний.")

    # Оновлення тексту в меню
    await update_menu_text(query)

    if data == NEXT_BUTTON:
        await query.message.edit_text(
            text=SECOND_MENU,
            parse_mode=ParseMode.HTML,
            reply_markup=SECOND_MENU_MARKUP
        )
    elif data == BACK_BUTTON:
        await query.message.edit_text(
            text=FIRST_MENU,
            parse_mode=ParseMode.HTML,
            reply_markup=FIRST_MENU_MARKUP
        )

async def update_menu_text(query):
    """Оновлення тексту меню відповідно до режиму."""
    status_text = "Бот запущено!" if bot_active else "Бот зупинено!"
    if screaming:
        status_text += "\nРежим капсу увімкнено!"
    else:
        status_text += "\nРежим капсу вимкнено!"

    # Оновлення тексту меню
    await query.message.edit_text(
        text=f"<b>Меню</b>\n{status_text}\n\n" + FIRST_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=FIRST_MENU_MARKUP
    )

async def scream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Функція для команди /scream."""
    global screaming
    screaming = True
    await context.bot.send_message(
        chat_id=update.message.chat.id,  # Відправка повідомлення в групу про стан капсу
        text="Режим капсу увімкнено!"
    )
    await update_menu_text(update)

async def whisper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Функція для команди /whisper."""
    global screaming
    screaming = False
    await context.bot.send_message(
        chat_id=update.message.chat.id,  # Відправка повідомлення в групу про стан капсу
        text="Режим капсу вимкнено!"
    )
    await update_menu_text(update)

def main() -> None:
    """Основна функція для запуску бота."""
    # Запит токену бота у користувача
    bot_token = input("Введіть токен бота: ")

    application = Application.builder().token(bot_token).build()

    # Реєстрація команд
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("scream", scream))
    application.add_handler(CommandHandler("whisper", whisper))

    # Обробка натискань кнопок
    application.add_handler(CallbackQueryHandler(button_tap))

    # Обробка будь-яких текстових повідомлень
    application.add_handler(MessageHandler(~filters.COMMAND, echo))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()