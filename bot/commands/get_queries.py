from telegram.parsemode import ParseMode

from bot.commands import BaseCommand

import mongo


class GetQueriesCommand(BaseCommand):

    _COMMAND = 'get_queries'
    _DESCRIPTION = 'Get your stop-words'

    def _call(self, bot, update, **kwargs):
        queries = mongo.get_queries(update.message.chat.id)
        if not queries:
            update.message.reply_text('You have no queries')
            return

        queries = ', '.join(sorted(
            '*{}*'.format(q)
            for q in queries
        ))

        update.message.reply_text(
            'Your queries are: {}'.format(queries),
            parse_mode=ParseMode.MARKDOWN,
        )
        return True
