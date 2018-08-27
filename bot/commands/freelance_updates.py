from telegram.parsemode import ParseMode

from bot.commands import BaseCommand
import mongo


class FreelanceUpdateCommand(BaseCommand):
    _COMMAND = 'freelance_updates'
    _DESCRIPTION = 'Get new projects from freelance markets'

    @staticmethod
    def _format_projects(projects):
        def _format_single_project(p):
            p['market'] = p['market'].title()

            t = (
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
        projects = mongo.get_new_projects(update.message.chat.id)
        if not projects:
            update.message.reply_text('No new projects found')
            return

        last_seen_projects = {}
        for project in projects:
            last_seen_projects[project['market']] = max((
                last_seen_projects.get(project['market'], 0),
                project['project_id'],
            ))

        text = self._format_projects(projects)
        update.message.reply_text(
            '{}\n\nSend /{} for more projects'.format(text, self._COMMAND.replace('_', '\_')),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        mongo.update_last_seen_projects(update.message.chat.id, last_seen_projects)
        return True
