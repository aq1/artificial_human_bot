from bot.commands import BaseCommand


class StartCommand(BaseCommand):

    _COMMAND = 'start'
    _SUCCESS_MESSAGE = 'Hello there.'


start_command = StartCommand().get()
