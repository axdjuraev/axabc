import logging
from typing import Protocol, runtime_checkable, Any, Union
from .simple_file_logger import SimpleFileLogger
from .logger_with_id import LogResult as _LogResult
from dataclasses import dataclass
from uuid import uuid4


@runtime_checkable
class Bot(Protocol):
    async def send_message(self, chat_id: int, message: str, parse_mode: str):
        raise NotImplementedError


@dataclass
class LogResult(_LogResult):
    message: Union[Any, None]
    message_id: Union[int, None]


class BotLogger(SimpleFileLogger):
    def __init__(self, name, bot: Bot, chat_id: int, level=logging.DEBUG, filename=..., hidden_url='https://google.com'):
        super().__init__(name, level, filename)

        if not isinstance(bot, Bot):
            raise NotImplementedError('bot object is not valid instance of Bot')

        self.bot = bot
        self.chat_id = chat_id
        self.parse_mode = 'Markdown'
        self.hidden_url = hidden_url
        self.limit = 4000

    async def send_event(self, msg: str, chat_id: int = ..., **kwargs) -> Any:
        if chat_id is ...:
            chat_id = self.chat_id

        return await self.bot.send_message(chat_id, msg, parse_mode=self.parse_mode, **kwargs)

    async def info(self, msg, stream_only=False, chat_id: int = ..., *args, **kwargs):
        return await self.log(logging.INFO, msg, stream_only, chat_id, *args, **kwargs)

    async def warning(self, msg, stream_only=False, chat_id: int = ..., *args, **kwargs):
        return await self.log(logging.WARNING, msg, stream_only, chat_id, *args, **kwargs)

    async def error(self, msg, stream_only=False, chat_id: int = ..., *args, **kwargs):
        return await self.log(logging.ERROR, msg, stream_only, chat_id, *args, **kwargs)

    async def critical(self, msg, stream_only=False, chat_id: int = ..., *args, **kwargs):
        return await self.log(logging.CRITICAL, msg, stream_only, chat_id, *args, **kwargs)

    async def log(self, level, msg, stream_only=False, chat_id: int = ..., *args, **kwargs):
        unique_id = uuid4()
        magic_url = f"{self.hidden_url}/{unique_id}"
        message = None
        message_id = None

        if not stream_only:
            bot_msg = msg[:self.limit] + '...' if len(msg) > self.limit else msg
            bot_msg = f'{bot_msg}[.]({magic_url})'
            message = await self.send_event(bot_msg, chat_id, **kwargs)
            message_id = message.id if hasattr(message, 'id') else message.message_id

        log_msg = f"{msg} [MESSAGE_ID: {message_id}]"
        self._log(level, log_msg, args, unique_id=unique_id, **kwargs)

        return LogResult(unique_id, log_msg, message, message_id)
