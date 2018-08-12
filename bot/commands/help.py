from bot.commands import BaseCommand


class HelpCommand(BaseCommand):

    _COMMAND = 'help'
    _SUCCESS_MESSAGE = 'Help message'


help_command = HelpCommand().get()
