from bot.commands import BaseCommand

import mongo


class AddDailyTaskCommand(BaseCommand):

    _COMMAND = 'add_daily_task'
    _success_message = 'Daily task added'
    _DESCRIPTION = 'Add a task with daily notification.'

    def _call(self, update, context):
        if not context.args:
            update.message.reply_text('Task name is required.')
            return

        mongo.daily_tasks.add_task(
            update.message.chat.id,
            context.args[0],
        )
        return True
