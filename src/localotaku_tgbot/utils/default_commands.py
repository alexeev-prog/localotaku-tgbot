from aiogram.types import BotCommand, BotCommandScopeDefault


async def setup_default_commands(bot):
    """
    Setup default bot commands

    :param		bot:  Bot
    :type		bot:  bot
    """
    commands = [
        BotCommand(command="start", description="Стартовать"),
        BotCommand(command="library", description="Показать библиотеку"),
        BotCommand(command="newanime", description="Добавить аниме в библиотеку"),
        BotCommand(command="editanime", description="Изменить аниме в библиотеке"),
        BotCommand(command="delanime", description="Удалить аниме из библиотеки"),
        BotCommand(command="shareanime", description="Поделиться аниме"),
        BotCommand(command="sharelib", description="Поделиться библиотекой аниме"),
        BotCommand(command="loadlib", description="Скачать библиотеку аниме"),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
