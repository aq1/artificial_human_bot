import random

import telegram
import requests

from bs4 import BeautifulSoup

import mongo
from bot.commands import (
    AdminBaseCommand,
    BaseCommand,
)


emojis = {}


class UpdateEmojisCommand(AdminBaseCommand):

    _COMMAND = 'update_emojis'
    _SUCCESS_MESSAGE = 'Updated emojis'

    @staticmethod
    def update_emojis():
        html = BeautifulSoup(
            requests.get('http://kaomoji.ru/en/').text,
            features='lxml',
        )

        tags = zip(
            html.find_all('h3'),
            html.find_all('table', {'class': 'table_kaomoji'}),
        )

        for name, table in tags:
            parsed_emojis = []
            for tr in table.find_all('tr'):
                for td in tr.find_all('td'):
                    parsed_emojis.append(td.text)
                    break
            if parsed_emojis:
                emojis[name.text.lower()] = parsed_emojis

    def _call(self, bot, update, **kwargs):
        try:
            self.update_emojis()
        except Exception as e:
            bot.send_message(
                update.message.chat.id,
                text=str(e),
                parse_mode=telegram.ParseMode.HTML,
            )
            return False

        return True


class BaseEmojiCommand(BaseCommand):

    def _call(self, bot, update, **kwargs):
        bot.send_message(
            update.message.chat.id,
            text=random.choice(emojis[self._COMMAND]),
            parse_mode=telegram.ParseMode.HTML,
        )
        return True


UpdateEmojisCommand.update_emojis()


def create_emoji_commands():

    def _emoji_command(name):
        class EmojiCommand(BaseEmojiCommand):
            _COMMAND = name.lower()
            _DESCRIPTION = 'Random {} emoji'.format(name.lower())

        return EmojiCommand

    commands = [
        _emoji_command(command)()
        for command in emojis.keys()
    ]

    return commands
