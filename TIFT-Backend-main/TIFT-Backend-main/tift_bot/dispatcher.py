from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from core.utils import TOKEN

dp = Dispatcher(storage=MemoryStorage())

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
