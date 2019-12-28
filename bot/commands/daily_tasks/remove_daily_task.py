from telegram import InlineKeyboardMarkup

from bot.commands import BaseCommand

import mongo


class RemoveDailyTaskCommand(BaseCommand):

    _COMMAND = 'remove_daily_task'
    _DESCRIPTION = 'Remove a daily task.'

    def _call(self, update, context):
        if not context.args:
            update.message.reply_text('Task name is required.')
            return

        if not mongo.daily_tasks.remove_task(update.message.chat.id, context.args[0]):
            update.message.reply_text('No task with name {} found'.format(context.args[0]))

        update.message.reply_text(
            text='Daily task removed',
        )
        return True

    def _callback_query_execute(self, bot, update, **kwargs):
        from bot.commands.daily_tasks import common

        mongo.daily_tasks.remove_task(
            update.callback_query.message.chat.id,
            update.callback_query.data.split()[1],
        )

        reply_markup = common.get_tasks_markup(update.callback_query.message.chat.id)
        text = common.get_tasks_list_text()
        if not reply_markup:
            text = 'No tasks left'

        update.callback_query.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(reply_markup),
        )
        return True
