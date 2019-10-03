import random

import telegram
import requests

from bs4 import BeautifulSoup

import settings
from bot.commands import (
    AdminBaseCommand,
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
