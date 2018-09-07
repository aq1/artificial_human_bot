from bot.commands.info.start import StartCommand
from bot.commands.info.help import HelpCommand
from bot.commands.info.bot_ip import BotIPCommand
from bot.commands.info.poloniex_balance import PoloniexBalanceCommand
from bot.commands.info.my_chat_id import MyChatIDCommand


def get_commands():
    return [
        StartCommand(),
        HelpCommand(),
        BotIPCommand(),
        PoloniexBalanceCommand(),
        MyChatIDCommand(),
    ]
