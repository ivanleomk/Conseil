import asyncio
from typing import List
from modal import Image, Stub, web_endpoint, Secret
import fastapi
import json
from lib.db import delete_todo, get_all_tasks, get_filtered_tasks
from lib.gpt import generate_actionables, parse_user_message
from lib.models.db import TodoItem
from lib.models.gpt import UserQuery
from lib.models.telegram_payload import (
    CallbackQuery,
    TelegramMessagePayload,
    VoiceMessagePayload,
)
from lib.telebot_helpers import get_bot, send_actionable_message
from lib.whisper import transcribe_voice_message

image = (
    Image.debian_slim()
    .apt_install("ffmpeg")
    .pip_install(
        "requests",
        "pydub",
        "python-telegram-bot",
        "pydantic==2.4.2",
        "instructor",
        "fastapi~=0.104.1",
    )
)

stub = Stub("transcriber", image=image)


@stub.function(
    secrets=[
        Secret.from_name("telebot"),
        Secret.from_name("cloudflare-ai"),
        Secret.from_name("cloudflare-db"),
        Secret.from_name("openai"),
    ]
)
@web_endpoint(method="POST")
async def transcribe(request: fastapi.Request):
    # Parse the request body
    body = await request.body()
    data = json.loads(body)
    print(f"Recieved payload of {data}")
    # We want to see what sort of message we have
    if "message" in data and "voice" in data["message"]:
        print("Matching on Whisper")
        # This is a whisper transcription
        await transcribe_voice_message(VoiceMessagePayload.model_validate(data))

        return {"statusCode": 200}
    if "message" in data and "entities" in data["message"]:
        # We have a command call
        parsed_payload = TelegramMessagePayload.model_validate(data)

        if "/help" in parsed_payload.message.text:
            bot = get_bot()
            await bot.send_message(
                chat_id=parsed_payload.message.chat.id,
                text="Welcome to Conseil, a one stop solution for you to collect all your thoughts. To get started, simply send us a voice message and we'll be good to go.",
            )
            return {"status": 200}
        elif "/outstanding" in parsed_payload.message.text:
            res = "*Outstanding tasks*"

            # No User Query specified
            if parsed_payload.message.text == "/outstanding":
                todos: List[TodoItem] = get_all_tasks()
            else:
                user_message = parsed_payload.message.text.replace("/outstanding", "")
                user_query: UserQuery = parse_user_message(user_message)
                todos: List[TodoItem] = get_filtered_tasks(user_query)

                res += f"\nYour query was *{user_message}*. Based on that, we identified the following Todos with the parameters"

                res += "" if not user_query.start else f"\n-start={user_query.start}\n"
                res += "" if not user_query.end else f"\n-end={user_query.end}\n"
                res += (
                    ""
                    if not user_query.completed
                    else f"\n-completed={user_query.completed}\n"
                )

            # Now we format everything
            if not todos:
                bot = get_bot()
                await bot.send_message(
                    chat_id=parsed_payload.message.chat.id,
                    text=f"No todos were found matching the query of *{parsed_payload.message.text.replace('/outstanding', '')}*",
                    parse_mode="Markdown",
                )
                return {"status": 200}

            for todo in todos:
                res += f"\n-{todo.title} : {todo.description}\n"

            bot = get_bot()
            await bot.send_message(
                chat_id=parsed_payload.message.chat.id, text=res, parse_mode="Markdown"
            )
            return {"status": 200}

    elif "callback_query" in data:
        print("Matching on Callback")
        # This is a callback query
        parsed_data = CallbackQuery.model_validate(data)

        # Now we match on the callback
        command = parsed_data.callback_query.data

        if command == "Generate Actionables":
            tasks = generate_actionables(parsed_data.callback_query.message.text)

            if not tasks:
                await get_bot().send_message(
                    chat_id=parsed_data.callback_query.message.chat.id,
                    text="Unable to identify any actionables",
                )

            tasks_send_actionables = [
                send_actionable_message(
                    task, parsed_data.callback_query.message.chat.id
                )
                for task in tasks
            ]
            await asyncio.gather(*tasks_send_actionables)
            print(f"Finished execution with tasks {tasks} idenitified")
        elif "Delete Item-" in command:
            # Delete the relevant Item from the DB
            delete_todo(command.replace("Delete Item-", ""))
            # Get the bot instance
            bot = get_bot()
            # Delete the telegram message
            try:
                await bot.delete_message(
                    chat_id=parsed_data.callback_query.message.chat.id,
                    message_id=parsed_data.callback_query.message.message_id,
                )
            except Exception as e:
                print(f"Encountered {e} - User might have clicked multiple times")

        return {"status_code": "Ok"}
    else:
        print("Unable to find a match")
        return {"status_code": "Ok"}
