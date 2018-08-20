import telegram.ext

from bot.commands import BaseCommand
import mongo


class FreelanceUpdateCommand(BaseCommand):
    _COMMAND = 'freelance_update'
    _DESCRIPTION = 'Get updates on freelance markets search'

    @staticmethod
    def _send_projects(update, projects):
        pass

    def _call(self, bot, update, **kwargs):
        user = mongo.get_user(update.message.chat.id)
        if not kwargs['args']:
            update.message.reply_text('Query required')
            return

        query = kwargs['args'][0]
        projects = list(
            mongo.get_projects(
                user,
                query,
            )
        )
        if not projects:
            update.message.reply_text('No projects found')
            return

        self._send_projects(update, projects)
        return True

    def get(self):
        return telegram.ext.CommandHandler(
            self._COMMAND,
            self.__call__,
            pass_args=True,
            pass_user_data=True,
        )
