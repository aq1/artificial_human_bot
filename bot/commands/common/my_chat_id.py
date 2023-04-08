from bot.commands import (
    BaseCommand,
)


class MyChatIDCommand(BaseCommand):

    _COMMAND = 'my_chat_id'
    _DESCRIPTION = 'Get your telegram ID'

    def _call(self, update, context):
        update.message.reply_text(
            text='Your chat is {}'.format(update.effective_chat.id),
        )
        return True
