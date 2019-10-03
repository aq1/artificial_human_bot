import random

import telegram
import requests

from bs4 import BeautifulSoup

import mongo
from bot.commands import (
    AdminBaseCommand,
    BaseCommand,
)


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
        emojis = []
        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                emojis.append(td.text)
                break
        if emojis:
            mongo.emojis.update_emojis(name, emojis)


class UpdateEmojisCommand(AdminBaseCommand):

    _COMMAND = 'update_emojis'
    _SUCCESS_MESSAGE = 'Updated emojis'

    def _call(self, bot, update, **kwargs):
        try:
            update_emojis()
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
            text=random.choice(
                mongo.emojis.get_emojis(
                    self._COMMAND
                )['emojis']
            ),
            parse_mode=telegram.ParseMode.HTML,
        )
        return True


def create_emoji_commands():

    def _emoji_command(name):
        class EmojiCommand(BaseEmojiCommand):
            _COMMAND = name

        return EmojiCommand

    commands = [
        _emoji_command(command['_id'])
        for command in mongo.emojis.get_emojis()
    ]

    return commands
