import random
import telegram

from bot.commands import BaseCommand


class LennyCommand(BaseCommand):

    _COMMAND = 'lenny'
    _SUCCESS_MESSAGE = '( ͡° ͜ʖ ͡°)'

    _DESCRIPTION = 'Gives you {}'.format(_SUCCESS_MESSAGE)

    def _call(self, bot, update, **kwargs):
        if str(update.message.from_user.id) != '387116733':
            return True

        if random.randint(0, 2) == 0:
            return True

        bot.send_message(
            update.message.chat_id,
            text='Ой, Федя иди нафиг',
            parse_mode=telegram.ParseMode.MARKDOWN,
        )
        return False
