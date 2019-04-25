from bot.commands import BaseCommand


class ShruggieCommand(BaseCommand):

    _COMMAND = 'shruggie'
    _SUCCESS_MESSAGE = r'¯\\_(ツ)\_/¯'

    _DESCRIPTION = 'Gives you {}'.format(_SUCCESS_MESSAGE)
