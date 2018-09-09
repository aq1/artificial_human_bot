from bot.commands import (
    BaseCommand,
)

import mongo


class SaveCommand(BaseCommand):

    _COMMAND = 'save'
    _DESCRIPTION = 'Save text to storage'
    _SUCCESS_MESSAGE = 'Text saved'

    def _call(self, bot, update, **kwargs):
        text = kwargs['args']
        if not text:
            update.message.reply_text(
                text='Text is required'
            )
            return False

        mongo.users.add_to_storage(update.message.chat.id, text[0])
        return True
