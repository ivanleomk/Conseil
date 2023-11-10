from modal import Image, Stub, web_endpoint, Secret
import fastapi
import json
import requests
import os
from pydub import AudioSegment
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater

image = (
    Image.debian_slim()
    .apt_install("ffmpeg")
    .pip_install("requests", "pydub", "python-telegram-bot")
)

stub = Stub("transcriber", image=image)


async def send_message(message, chatId):
    TOKEN = os.environ["TOKEN"]
    bot = Bot(token=TOKEN)

    keyboard = [[InlineKeyboardButton("Generate Actionables", callback_data="1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(chat_id=chatId, text=message, reply_markup=reply_markup)


@stub.function(secrets=[Secret.from_name("telebot"), Secret.from_name("cloudflare-ai")])
@web_endpoint(method="POST")
async def transcribe(request: fastapi.Request):
    # Parse the request body
    body = await request.body()
    data = json.loads(body)
    # We only want to process voice messages
    if "voice" not in data["message"]:
        print("Invalid message type")
        return

    fileId = data["message"]["voice"]["file_id"]
    chatId = data["message"]["chat"]["id"]
    TOKEN = os.environ["TOKEN"]
    print(f"Processing fileId of {fileId}")
    fileAddress = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={fileId}"
    # We first get the file address
    filePathResponse = requests.get(fileAddress)
    fileResponse = filePathResponse.json()
    filePath = fileResponse["result"]["file_path"]

    # Then we download the file path
    fileUrl = f"https://api.telegram.org/file/bot{TOKEN}/{filePath}"
    fileBytes = requests.get(fileUrl)

    fileName = filePath.replace("voice/", "")
    with open(fileName, "wb") as file:
        file.write(fileBytes.content)

    oga_audio = AudioSegment.from_ogg(fileName)

    # Now we pass the names to our transcriber
    # # Export as .mp3
    oga_audio.export(fileName.replace(".oga", ".mp3"), format="mp3")

    # Now we fire off a request to cloudflare
    ACCOUNT_ID = os.environ["ACCOUNT_ID"]
    API_TOKEN = os.environ["API_TOKEN"]

    # Break down the .mp3 into 30 second chunks with 1s overlap
    audio = AudioSegment.from_mp3(fileName.replace(".oga", ".mp3"))
    chunks = [audio[i : i + 30000] for i in range(0, len(audio), 29000)]

    async def send_chunk(i, chunk):
        # Convert chunk to mp3 format directly into the data of the response
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/openai/whisper",
            headers=headers,
            data=chunk.export(format="mp3"),
        )

        data = response.json()
        return data["result"]["text"]

    # Send these chunks to the endpoint
    tasks = [send_chunk(i, chunk) for i, chunk in enumerate(chunks)]
    results = await asyncio.gather(*tasks)

    await send_message(" ".join(results), chatId)
    return {"statusCode": 200}
