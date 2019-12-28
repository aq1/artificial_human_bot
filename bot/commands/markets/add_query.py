from bot.commands import BaseCommand

import mongo


class AddQueryCommand(BaseCommand):

    _COMMAND = 'add_query'
    _success_message = 'Query added'
    _DESCRIPTION = 'Add a stop-word for the search by freelance markets'

    def _call(self, update, context):
        if not context.args:
            update.message.reply_text('Query text is required.')
            return

        mongo.users.add_query(update.message.chat.id, context.args[0])
        return True
