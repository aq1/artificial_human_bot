from bot.commands import BaseCommand


class HelpCommand(BaseCommand):

    _COMMAND = 'help'
    _SUCCESS_MESSAGE = 'Help message'

    _DESCRIPTION = 'Show available commands'
