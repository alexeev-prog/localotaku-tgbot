from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from localotaku_tgbot.config import ConfigurationManager

config = ConfigurationManager("lotgbot_cfg.toml").config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())
