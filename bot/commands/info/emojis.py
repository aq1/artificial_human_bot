import random

import telegram

import settings
from bot.commands import (
    BaseCommand,
)


class BaseEmojiCommand(BaseCommand):

    def _call(self, bot, update, **kwargs):
        bot.send_message(
            update.message.chat.id,
            text=random.choice(settings.EMOJIS[self._COMMAND]),
            parse_mode=telegram.ParseMode.HTML,
        )
        return True


class ListEmojis(BaseCommand):

    _COMMAND = 'emojis'
    _DESCRIPTION = 'Get list of emojis'

    @property
    def success_message(self):
        emojis = list(settings.EMOJIS.keys())
        text = '\n'.join([
            '\t'.join(emojis[i:i + 3]) for i in range(0, len(emojis), 3)
        ])
        return text


def create_emoji_commands():

    def _emoji_command(name):
        class EmojiCommand(BaseEmojiCommand):
            _COMMAND = name.lower()
            _DESCRIPTION = 'Random {} emoji'.format(name.lower())

        return EmojiCommand

    commands = [
        _emoji_command(command)()
        for command in settings.EMOJIS.keys()
    ]

    return commands