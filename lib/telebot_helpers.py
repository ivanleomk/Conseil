import os
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from lib.db import insert_todo
from datetime import datetime
from lib.models.gpt import Actionable


def get_bot():
    if not os.environ["TOKEN"]:
        raise ValueError("Unable to detect an environment variable of TOKEN")

    return Bot(token=os.environ["TOKEN"])


async def reply_to_whisper_transcription(message, chatId):
    bot = get_bot()

    keyboard = [
        [
            InlineKeyboardButton(
                "Generate Actionables", callback_data="Generate Actionables"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(chat_id=chatId, text=message, reply_markup=reply_markup)


async def send_actionable_message(actionable: Actionable, chatId: str):
    bot = get_bot()
    # We insert into the DB and then get back an ID (This way we use soft inserts, we can also do some logging of generated metadata prior to this)
    res = insert_todo(actionable)

    # We then generate a DB Id
    keyboard = [
        [
            InlineKeyboardButton(
                "Delete Item", callback_data=f"Delete Item-{res.todoId}"
            ),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    due_date = datetime.strptime(actionable.due_date, "%Y-%m-%d")
    due_date_formatted = due_date.strftime("%d %B %Y")
    today = datetime.today()
    days_remaining = (due_date - today).days
    await bot.send_message(
        chat_id=chatId,
        text=f"*Task*: {actionable.title}\n*Due Date*: {due_date_formatted} ( in {days_remaining} days)\n*Description*: {actionable.description}",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )
