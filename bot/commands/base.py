import telegram.ext

import settings
import mongo
import bot


class BaseCommand(telegram.ext.CommandHandler):

    _COMMAND = ''
    _RETURN_STATE = bot.states.START

    _SUCCESS_MESSAGE = ''

    _DESCRIPTION = ''

    def __init__(self,
                 command=None,
                 callback=None,
                 filters=None,
                 allow_edited=False,
                 pass_args=False,
                 pass_update_queue=False,
                 pass_job_queue=False,
                 pass_user_data=False,
                 pass_chat_data=False):

        command = command or self._COMMAND
        callback = callback or self.__call__

        super().__init__(command,
                         callback,
                         filters,
                         allow_edited,
                         pass_args,
                         pass_update_queue,
                         pass_job_queue,
                         pass_user_data,
                         pass_chat_data)

    @classmethod
    def get_command(cls, markdown=False):
        command = '/{}'.format(cls._COMMAND)
        if markdown:
            command = command.replace('_', '\_')
        return command

    def _allowed_to_execute(self, bot, update):
        return True

    @property
    def _success_message(self):
        return self._SUCCESS_MESSAGE

    def _callback_query_execute(self, bot, update, **kwargs):
        return True

    def callback_query(self, bot, update, **kwargs):
        """
        Similar to __call__ logic, but for inline buttons callbacks
        """
        mongo.users.save_user(update.callback_query.message.chat)

        if not self._allowed_to_execute(bot, update):
            return

        ok = self._callback_query_execute(bot, update, **kwargs)

        if ok and self._success_message:
            bot.send_message(
                update.callback_query.message.chat.id,
                text=self._success_message,
            )

        return self._RETURN_STATE

    def _call(self, bot, update, **kwargs):
        """
        Return bool indicating successful execution
        """
        return True

    @telegram.ext.dispatcher.run_async
    def __call__(self, bot, update, **kwargs):
        if update.callback_query:
            return self.callback_query(bot, update, **kwargs)

        mongo.users.save_user(update.message.chat)

        if not self._allowed_to_execute(bot, update):
            return

        ok = self._call(bot, update, **kwargs)

        if ok and self._success_message:
            update.message.reply_text(
                text=self._success_message,
                parse_mode=telegram.ParseMode.MARKDOWN,
            )

        return self._RETURN_STATE

    def __str__(self):
        return '{} - {}'.format(self._COMMAND, self._DESCRIPTION)


class AdminPermissionMixin:

    def _allowed_to_execute(self, bot, update):
        message = update.message or update.callback_query.message
        return message.chat.id in settings.ADMINS

    def __str__(self):
        return ''
