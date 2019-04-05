from bot.commands import BaseCommand


class HelpCommand(BaseCommand):

    _COMMAND = 'help'
    _SUCCESS_MESSAGE = 'Nobody can help you apart from yourself'

    _DESCRIPTION = 'Help'
