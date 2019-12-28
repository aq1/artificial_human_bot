from bot.commands import (
    BaseCommand,
)

import mongo


class ListStorageCommand(BaseCommand):

    _COMMAND = 'list_storage'
    _DESCRIPTION = 'Get all your storage'

    def _call(self, update, context):

        text = '\n'.join(mongo.users.list_storage(update.message.chat.id))
        if not text:
            text = 'Storage is empty'
        else:
            text = 'Your storage\n{}'.format(text)
        update.message.reply_text(
            text,
            disable_web_page_preview=True,
        )
        return True
