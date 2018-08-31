import telegram
import telegram.ext

import settings
import bot
import mongo
from utils.logging import logger

commands = [
    bot.commands.common.StartCommand(),
    bot.commands.common.HelpCommand(),
    bot.commands.markets.FreelanceUpdateCommand(pass_args=True, pass_user_data=True),
    bot.commands.markets.GetQueriesCommand(),
    bot.commands.markets.AddQueryCommand(pass_args=True, pass_user_data=True),
    bot.commands.markets.RemoveQueryCommand(pass_args=True, pass_user_data=True),
]

bot_handler = telegram.ext.ConversationHandler(
    entry_points=commands,
    states={
        bot.states.START: commands,
    },
    fallbacks=[telegram.ext.RegexHandler('\w+', lambda *args: bot.states.START)]
)


def notify_users_about_restart(_bot):
    for user in mongo.users.get_all_user():
        _bot.send_message(
            chat_id=user['chat_id'],
            text='I am working now.'
        )


def start_bot():
    _bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    updater = telegram.ext.Updater(bot=_bot)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(bot_handler)
    logger.info('Printing available commands')
    logger.info('\n'.join(map(str, commands)))
    logger.info('Started Bot')
    notify_users_about_restart(_bot)
    try:
        updater.start_polling(clean=True)
    except KeyboardInterrupt:
        logger.info('Stopped Bot')
