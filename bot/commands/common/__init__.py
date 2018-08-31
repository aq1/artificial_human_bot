from bot.commands.common.base import BaseCommand
from bot.commands.common.start import StartCommand
from bot.commands.common.help import HelpCommand


def get_commands():
    return [
        StartCommand(),
        HelpCommand(),
    ]
