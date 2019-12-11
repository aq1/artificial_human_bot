from bot.commands import (
    BaseCommand,
)


class ShameCommand(BaseCommand):

    _COMMAND = 'shame'
    _DESCRIPTION = 'Shame user because of immoral behavior'

    def _call(self, bot, update, **kwargs):
        print(kwargs['args'])
        return True
