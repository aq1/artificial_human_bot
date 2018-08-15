import telegram
import telegram.ext

import settings
import bot
from utils.logging import logger

commands = [
    bot.commands.start_command,
    bot.commands.help_command,
    bot.commands.freelance_update_command,
]

bot_handler = telegram.ext.ConversationHandler(
    entry_points=commands,
    states={
        bot.states.START: commands,
    },
    fallbacks=[telegram.ext.RegexHandler('\w+', lambda *args: bot.states.START)]
)


def start_bot():
    _bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    updater = telegram.ext.Updater(bot=_bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(bot_handler)
    logger.info('Started Bot')
    try:
        updater.start_polling(clean=True)
    except KeyboardInterrupt:
        logger.info('Stopped Bot')
