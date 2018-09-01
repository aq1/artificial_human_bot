from bot.commands import BaseCommand

import mongo


class AddDailyTaskCommand(BaseCommand):

    _COMMAND = 'add_daily_task'
    _success_message = 'Daily task added'
    _DESCRIPTION = 'Add a task with daily notification.'

    def _call(self, bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Task name is required.')
            return

        mongo.daily_tasks.add_task(
            update.message.chat.id,
            kwargs['args'][0],
        )
        return True
