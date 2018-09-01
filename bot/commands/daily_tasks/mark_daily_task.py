from bot.commands import BaseCommand

import mongo


class MarkDailyTaskCommand(BaseCommand):

    _COMMAND = 'mark_daily_task'
    _DESCRIPTION = 'Mark your daily tasks complete/incomplete'

    def _call(self, bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Task name is required.')
            return

        mongo.daily_tasks.add_task(
            update.message.chat.id,
            kwargs['args'][0],
        )
        return True
