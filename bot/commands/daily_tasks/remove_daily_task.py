from bot.commands import BaseCommand

import mongo


class RemoveDailyTaskCommand(BaseCommand):

    _COMMAND = 'remove_daily_task'
    _success_message = 'Daily task removed'
    _DESCRIPTION = 'Remove a daily task.'

    def _call(self, bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Task name is required.')
            return

        if not mongo.daily_tasks.remove_task(update.message.chat.id, kwargs['args'][0]):
            update.message.reply_text('No task with name {} found'.format(kwargs['args'][0]))

        return True

    def _callback_query_execute(self, bot, update, **kwargs):
        mongo.daily_tasks.remove_task(
            update.callback_query.message.chat.id,
            update.callback_query.data.split()[1],
        )

        return True
