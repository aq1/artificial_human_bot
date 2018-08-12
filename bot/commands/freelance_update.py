import telegram.ext

from bot.commands import BaseCommand
from utils import mongo


class FreelanceUpdateCommand(BaseCommand):
    _COMMAND = 'freelance_update'

    @staticmethod
    def _send_projects(update, projects):
        pass

    def _call(self, bot, update, **kwargs):
        query = kwargs['args'][0] if kwargs['args'] else None
        user = mongo.get_user(update.message.chat.id)
        projects = list(
            mongo.get_projects(
                query,
                user['last_project_time'],
                kwargs['user_data'].get('skip', 0),
            )
        )
        if not projects:
            return update.message.reply_text('No projects found')
        return self._send_projects(update, projects)

    def get(self):
        return telegram.ext.CommandHandler(
            self._COMMAND,
            self.__call__,
            pass_args=True,
            pass_user_data=True,
        )


freelance_update_command = FreelanceUpdateCommand().get()
