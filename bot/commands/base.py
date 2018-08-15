import telegram.ext

import mongo
import bot


class BaseCommand:

    _COMMAND = ''
    _RETURN_STATE = bot.states.START

    _SUCCESS_MESSAGE = ''

    _DESCRIPTION = ''

    def _call(self, bot, update, **kwargs):
        """
        Return bool indicating successful execution
        """
        pass

    @telegram.ext.dispatcher.run_async
    def __call__(self, bot, update, **kwargs):
        mongo.save_user(update.message.chat)

        ok = self._call(bot, update, **kwargs)

        if ok and self._SUCCESS_MESSAGE:
            update.message.reply_text(self._SUCCESS_MESSAGE)

        return self._RETURN_STATE

    def get(self):
        return telegram.ext.CommandHandler(
            self._COMMAND,
            self.__call__,
        )
