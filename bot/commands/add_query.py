from bot.commands import BaseCommand

import mongo


class AddQueryCommand(BaseCommand):

    _COMMAND = 'add_query'
    _SUCCESS_MESSAGE = 'Query added'

    def _call(self, bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Query text required.')
            return
        mongo.add_query(update.message.chat.id, kwargs['args'][0])


add_query_command = AddQueryCommand().get()
