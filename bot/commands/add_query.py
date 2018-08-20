import telegram.ext

from bot.commands import BaseCommand

import mongo


class AddQueryCommand(BaseCommand):

    _COMMAND = 'add_query'
    _SUCCESS_MESSAGE = 'Query added'
    _DESCRIPTION = 'Add a stop-word for the search by freelance markets'

    def _call(self, bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Query text required.')
            return

        mongo.add_query(update.message.chat.id, kwargs['args'][0])
        return True
