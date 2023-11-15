import json
from telegram_payload import (
    CallbackQueryReplyMarkup,
    UserPayload,
    ChatPayload,
    CallbackQueryMessage,
    CallbackQueryBody,
    CallbackQuery,
    VoicePayload,
    VoiceMessagePayloadBody,
    VoiceMessagePayload,
    FileQueryPayload,
)


class TestFilePayloadModels:
    """
    This is a set of tests which we can use to accurately parse the data when we send a voice message over to the bot
    """

    def test_file_query_payload_deserialization(self):
        data = {
            "ok": True,
            "result": {
                "file_id": "1",
                "file_unique_id": "1",
                "file_path": "path/to/file",
                "file_size": 1000,
            },
        }
        payload = FileQueryPayload(**data)
        assert payload.ok
        assert payload.result.file_id == "1"
        assert payload.result.file_path == "path/to/file"
        assert payload.result.file_size == 1000


class TestWhisperPayloadModels:
    """
    This is a set of tests that validates that we can accurately parse the data when we send a voice message over to the bot
    """

    def test_voice_payload(self):
        sample_payload = """
        {
          "duration": 8,
          "mime_type": "audio/ogg",
          "file_id": "abc123",
          "file_unique_id": "abc123",
          "file_size": 32397
        }
        """
        parsed_voice_payload = VoicePayload.model_validate(json.loads(sample_payload))
        assert parsed_voice_payload.mime_type == "audio/ogg"
        assert parsed_voice_payload.file_id == "abc123"

    def test_voice_message_payload(self):
        sample_payload = """
        {
          "message_id": 123,
          "from": {
            "id": 123123,
            "is_bot": "False",
            "first_name": "user",
            "username": "username",
            "language_code": "en"
          },
          "chat": {
            "id": 12314,
            "first_name": "user",
            "username": "username",
            "type": "private"
          },
          "date": 12345,
          "voice": {
            "duration": 8,
            "mime_type": "audio/ogg",
            "file_id": "abcd123",
            "file_unique_id": "abcdef",
            "file_size": 32397
          }
        }
        """
        parsed_voice_payload_body = VoiceMessagePayloadBody.model_validate(
            json.loads(sample_payload)
        )
        assert parsed_voice_payload_body.date == 12345
        assert parsed_voice_payload_body.voice.duration == 8

    def test_voice_full_payload(self):
        sample_payload = """
        {
          "update_id": 12345,
          "message": {
            "message_id": 123123,
            "from": {
              "id": 123123123,
              "is_bot": "False",
              "first_name": "asasd",
              "username": "asdasd",
              "language_code": "en"
            },
            "chat": {
              "id": 123123123,
              "first_name": "asasd",
              "username": "asdasdas",
              "type": "private"
            },
            "date": 123123123,
            "voice": {
              "duration": 8,
              "mime_type": "audio/ogg",
              "file_id": "asdasdads",
              "file_unique_id": "asdasdasd",
              "file_size": 32397
            }
          }
        }
        """
        parsed_payload = VoiceMessagePayload.model_validate(json.loads(sample_payload))
        assert parsed_payload.update_id == 12345


class TestCallbackModels:
    """
    This is a set of tests that validates that we can accurately parse the data that will be sent over by Telegram when we attempt to use a callback query defined in a message
    """

    def test_callback_message(self):
        sample_payload = """
        {
          "update_id": 342322123123,
          "callback_query":{
          "id": "123123123",
          "from": {
          "id": 123123123123,
          "is_bot": "False",
          "first_name": "User",
          "username": "username",
          "language_code": "en"
          },
          "message": {
          "message_id": 11222,
          "from": {
              "id": 123123123,
              "is_bot": "True",
              "first_name": "sdasda",
              "username": "asdasdasd"
          },
          "chat": {
              "id": 123123123,
              "first_name": "asdasdasd",
              "username": "asdasdasdasd",
              "type": "private"
          },
          "date": 1231231213,
          "text": "asdasdadasdasdasd",
          "reply_markup": {
              "inline_keyboard": [
              [
                  {
                  "text": "Generate Actionables",
                  "callback_data": "1"
                  }
              ]
              ]
          }
          },
          "chat_instance": "123123123123123123",
          "data": "1"
        }
        }
        """
        CallbackQuery.model_validate(json.loads(sample_payload))

    def test_callback_query_message(self):
        sample_query_message = """
      {
          "id": "123123123",
          "from": {
          "id": 123123123123,
          "is_bot": "False",
          "first_name": "User",
          "username": "username",
          "language_code": "en"
          },
          "message": {
          "message_id": 11222,
          "from": {
              "id": 123123123,
              "is_bot": "True",
              "first_name": "sdasda",
              "username": "asdasdasd"
          },
          "chat": {
              "id": 123123123,
              "first_name": "asdasdasd",
              "username": "asdasdasdasd",
              "type": "private"
          },
          "date": 1231231213,
          "text": "asdasdadasdasdasd",
          "reply_markup": {
              "inline_keyboard": [
              [
                  {
                  "text": "Generate Actionables",
                  "callback_data": "1"
                  }
              ]
              ]
          }
          },
          "chat_instance": "123123123123123123",
          "data": "1"
      }
      """
        sample_callback_message = CallbackQueryBody.model_validate(
            json.loads(sample_query_message)
        )

    def test_callback_query_message_payload(self):
        sample_callback = """
        {
          "message_id": 123,
          "from": {
            "id": 12345,
            "is_bot": "true",
            "first_name": "abcdef",
            "username": "FUYOH"
          },
          "chat": {
            "id": 12345,
            "first_name": "User",
            "username": "username",
            "type": "private"
          },
          "date": 1234,
          "text": "This is sample text",
          "reply_markup": {
            "inline_keyboard": [
              [
                {
                  "text": "Generate Actionables",
                  "callback_data": "1"
                }
              ]
            ]
          }
        }
        """
        parsed_query_callback = CallbackQueryMessage.model_validate(
            json.loads(sample_callback)
        )
        assert parsed_query_callback.date == 1234

    def test_parsing_chat(self):
        sample_chat = """
        {
            "id": 12345,
            "first_name": "User",
            "username": "username",
            "type": "private"
        }
        """
        parsed_chat = ChatPayload.model_validate(json.loads(sample_chat))
        assert parsed_chat.id == 12345
        assert parsed_chat.type == "private"

    def test_parsing_from(self):
        sample_from = """
        {
                "id": 1234,
                "is_bot": "True",
                "first_name": "Conseil",
                "username": "FakeTelegramBot"
        }
        """
        parsed_from = UserPayload.model_validate(json.loads(sample_from))
        assert parsed_from.id == 1234

    def test_parsing_reply_markup(self):
        sample_markup = """
        {
            "inline_keyboard": [
              [
                {
                  "text": "Generate Actionables",
                  "callback_data": "1"
                }
              ]
            ]
        }
        """
        parsed_markup = CallbackQueryReplyMarkup.model_validate(
            json.loads(sample_markup)
        )
        assert len(parsed_markup.inline_keyboard) == 1
        assert len(parsed_markup.inline_keyboard[0]) == 1
        assert parsed_markup.inline_keyboard[0][0].callback_data == "1"
        assert parsed_markup.inline_keyboard[0][0].text == "Generate Actionables"
