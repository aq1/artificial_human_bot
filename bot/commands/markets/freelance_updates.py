from telegram.parsemode import ParseMode

from bot.commands import BaseCommand
import mongo


class FreelanceUpdateCommand(BaseCommand):
    _COMMAND = 'freelance_updates'
    _DESCRIPTION = 'Get new projects from freelance markets'

    @staticmethod
    def get_last_seen_projects(projects):
        last_seen_projects = {}
        for project in projects:
            last_seen_projects[project['market']] = max((
                last_seen_projects.get(project['market'], 0),
                project['project_id'],
            ))

        return last_seen_projects

    def _format_message(self, projects):
        return '{}\n\nSend {} for more projects'.format(projects, self.get_command(markdown=True))

    def get_message(self, projects):
        return self._format_message(self._format_projects(projects))

    @staticmethod
    def _format_projects(projects):
        def _format_single_project(p):
            p['market'] = p['market'].title()
            p['time_updated'] = p['time_updated'].replace('T', ' ')

            t = (
                '{p[time_updated]}\n'
                '*{p[market]}* {p[type]}\n'
                '[{p[title]}]({p[url]})\n'
                '${p[budget][min]} - ${p[budget][max]}'
            ).format(p=p).strip()

            if p.get('hourly_info'):
                t = '{}\n{} hours per {}'.format(
                    t,
                    p['hourly_info']['commitment']['hours'],
                    p['hourly_info']['commitment']['interval'],
                )

            return t

        text = []
        for project in projects:
            text.append(_format_single_project(project))

        return '\n\n'.join(text)

    def _call(self, bot, update, **kwargs):
        projects = mongo.projects.get_new_projects(update.message.chat.id)
        if not projects:
            update.message.reply_text('No new projects found')
            return

        last_seen_projects = self.get_last_seen_projects(projects)

        update.message.reply_text(
            self.get_message(projects),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        mongo.users.update_last_seen_projects(update.message.chat.id, last_seen_projects)
        return True
