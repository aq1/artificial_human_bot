import telegram
import telegram.ext

from bot.commands import (
    AdminBaseCommand,
)

from mongo import twitter


class AddTwitterAccountCommand(AdminBaseCommand):

    _SUCCESS_MESSAGE = 'Account added'
    _COMMAND = 'add_twitter_accounts'

    def _call(self, update: telegram.Update, context: telegram.ext.CallbackContext):
        update.effective_message.reply_text(
            text=str(context.args),
        )
        return True
