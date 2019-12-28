import re

import telegram.ext

import mongo


class ShizoCommand(telegram.ext.RegexHandler):
    COUNT = mongo.client.db.emojis.find_one({'_id': 'shizo'})['count']

    def _callback(self, bot, update):
        try:
            text = self.COUNT[(self.COUNT.index(update.message.text) + 1) % len(self.COUNT)]
        except ValueError:
            return
        bot.send_message(update.message.chat_id, text)

    def __init__(self, *args, **kwargs):
        super().__init__(
            pattern=re.compile(r'({})'.format('|'.join(self.COUNT)), flags=re.I | re.U),
            callback=self._callback,
        )
