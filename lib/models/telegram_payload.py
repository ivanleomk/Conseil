from typing import List, Literal
from pydantic import BaseModel, Field

ACCEPTED_ACTIONS = Literal["Generate Actionables", "Delete Item"]
ACCEPTED_FILETYPES = Literal["audio/ogg"]
ACCEPTED_CHAT_TYPES = Literal["private"]
ACCEPTED_COMMANDS = Literal["/help", "/outstanding"]


class InlineKeyboardAction(BaseModel):
    text: ACCEPTED_ACTIONS
    callback_data: str


class ChatPayload(BaseModel):
    id: int
    first_name: str
    username: str
    type: ACCEPTED_CHAT_TYPES


class UserPayload(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str = Field(default=None)


class VoicePayload(BaseModel):
    duration: int
    mime_type: ACCEPTED_FILETYPES
    file_id: str
    file_unique_id: str
    file_size: int


class CallbackQueryReplyMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboardAction]]


class CallbackQueryMessage(BaseModel):
    message_id: int
    from_user: UserPayload = Field(..., alias="from")
    chat: ChatPayload
    date: int
    text: str
    reply_markup: CallbackQueryReplyMarkup


class CallbackQueryBody(BaseModel):
    id: int
    chat_instance: int
    from_user: UserPayload = Field(alias="from")
    data: str
    message: CallbackQueryMessage


class VoiceMessagePayloadBody(BaseModel):
    message_id: int
    date: int
    from_user: UserPayload = Field(..., alias="from")
    chat: ChatPayload
    voice: VoicePayload


class FileQueryPayloadBody(BaseModel):
    file_id: str
    file_unique_id: str
    file_path: str
    file_size: int


# Actual Parent Bodies


class CallbackQuery(BaseModel):
    update_id: int
    callback_query: CallbackQueryBody


class VoiceMessagePayload(BaseModel):
    update_id: int
    message: VoiceMessagePayloadBody


class VoiceMessagePayloadBody(BaseModel):
    message_id: int
    date: int
    from_user: UserPayload = Field(..., alias="from")
    chat: ChatPayload
    voice: VoicePayload


class FileQueryPayload(BaseModel):
    ok: bool
    result: FileQueryPayloadBody


class TelegramCommandEntity(BaseModel):
    offset: int
    command_length: int = Field(..., alias="length")
    type: str


class TelegramMessageBody(BaseModel):
    message_id: int
    from_user: UserPayload = Field(..., alias="from")
    chat: ChatPayload
    date: int
    text: str
    entities: List[TelegramCommandEntity]


class TelegramMessagePayload(BaseModel):
    update_id: int
    message: TelegramMessageBody
