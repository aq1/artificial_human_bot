import random
import telegram

from bot.commands import BaseCommand


class LennyCommand(BaseCommand):

    _COMMAND = 'lenny'
    _SUCCESS_MESSAGE = '( ͡° ͜ʖ ͡°)'

    _DESCRIPTION = 'Gives you {}'.format(_SUCCESS_MESSAGE)
