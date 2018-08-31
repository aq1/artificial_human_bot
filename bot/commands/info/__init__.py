from bot.commands.info.base import BaseCommand
from bot.commands.info.start import StartCommand
from bot.commands.info.help import HelpCommand


def get_commands():
    return [
        StartCommand(),
        HelpCommand(),
    ]
