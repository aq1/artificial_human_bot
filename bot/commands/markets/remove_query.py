import telegram.ext

from bot.commands import BaseCommand

import mongo


class RemoveQueryCommand(BaseCommand):

    _COMMAND = 'remove_query'
    _SUCCESS_MESSAGE = 'Query removed'
    _DESCRIPTION = 'Remove a stop-word for the search by freelance markets'

    def _call(self, bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Query text required.')
            return
        mongo.users.remove_query(update.message.chat.id, kwargs['args'][0])
        return True

    def get(self):
        return telegram.ext.CommandHandler(
            self._COMMAND,
            self.__call__,
            pass_args=True,
            pass_user_data=True,
        )
