import re

import telegram.ext

import mongo

from bot.commands.base import BaseRegexHandler


class ShizoHandler(BaseRegexHandler):

    COUNT = mongo.client.db.emojis.find_one({'_id': 'shizo'})['count']
    REGEX = r'^({})$'.format('|'.join(COUNT))

    def _callback(self, update, context):
        try:
            text = self.COUNT[(self.COUNT.index(update.message.text.lower()) + 1) % len(self.COUNT)]
        except ValueError:
            return
        context.bot.send_message(update.message.chat_id, text)
