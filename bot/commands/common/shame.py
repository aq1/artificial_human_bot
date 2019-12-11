import telegram

from bot.commands import (
    BaseCommand,
)


class ShameCommand(BaseCommand):

    _COMMAND = 'shame'
    _DESCRIPTION = 'Shame user because of immoral behavior'

    def _call(self, bot, update, **kwargs):
        text = ' and '.join([
            update.message.text[e['offset']: e['offset'] + e['length']]
            for e in update.message.entities
            if e['type'] in {telegram.MessageEntity.MENTION, telegram.MessageEntity.TEXT_MENTION}
        ])

        if text:
            bot.send_message(
                chat_id=update.message.chat.id,
                text='Shame on {}!! Be ashamed!'.format(text),
            )
        return True
