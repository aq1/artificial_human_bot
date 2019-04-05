from bot.commands.info.start import StartCommand
from bot.commands.info.help import HelpCommand
from bot.commands.info.bot_ip import BotIPCommand
from bot.commands.info.poloniex_balance import PoloniexBalanceCommand
from bot.commands.info.my_chat_id import MyChatIDCommand
from bot.commands.info.lenny import LennyCommand
from bot.commands.info.shruggie import ShruggieCommand


def get_commands():
    return [
        StartCommand(),
        HelpCommand(),
        BotIPCommand(),
        PoloniexBalanceCommand(),
        MyChatIDCommand(),
        LennyCommand(),
        ShruggieCommand(),
    ]
