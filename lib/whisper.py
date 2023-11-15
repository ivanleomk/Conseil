import os
from pydub import AudioSegment
import asyncio
import requests
from lib.models.telegram_payload import VoiceMessagePayload, FileQueryPayload

from lib.telebot_helpers import reply_to_whisper_transcription

sem = asyncio.Semaphore(8)


def download_file(file_path: str):
    TOKEN = os.environ["TOKEN"]
    fileUrl = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    fileBytes = requests.get(fileUrl)

    fileName = file_path.replace("voice/", "")
    with open(fileName, "wb") as file:
        file.write(fileBytes.content)

    oga_audio = AudioSegment.from_ogg(fileName)

    # Now we pass the names to our transcriber
    # # Export as .mp3
    oga_audio.export(fileName.replace(".oga", ".mp3"), format="mp3")

    return fileName


async def transcribe_chunk(chunk):
    async with sem:
        ACCOUNT_ID = os.environ["ACCOUNT_ID"]
        API_TOKEN = os.environ["API_TOKEN"]
        # Convert chunk to mp3 format directly into the data of the response
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/openai/whisper",
            headers=headers,
            data=chunk.export(format="mp3"),
        )

        data = response.json()
        return data["result"]["text"]


async def transcribe_voice_message(data: VoiceMessagePayload):
    TOKEN = os.environ["TOKEN"]
    fileId = data.message.voice.file_id
    chatId = data.message.chat.id

    fileAddress = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={fileId}"
    # We first get the file address
    filePathResponse = requests.get(fileAddress)
    fileResponse = FileQueryPayload.model_validate(filePathResponse.json())
    file_path = fileResponse.result.file_path

    # Then we download the file path
    file_name = download_file(file_path)
    # Now we fire off a request to cloudflare

    # Break down the .mp3 into 30 second chunks with 1s overlap
    audio = AudioSegment.from_mp3(file_name.replace(".oga", ".mp3"))

    chunks = [audio[i : i + 30000] for i in range(0, len(audio), 29000)]
    tasks_transcribe_chunks = [transcribe_chunk(chunk) for chunk in chunks]
    resp = await asyncio.gather(*tasks_transcribe_chunks)

    await reply_to_whisper_transcription(" ".join(resp), chatId)
