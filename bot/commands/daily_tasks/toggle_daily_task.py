from telegram import InlineKeyboardMarkup

from bot.commands import BaseCommand

import mongo


class ToggleDailyTaskCommand(BaseCommand):

    _COMMAND = 'mark_daily_task'
    _DESCRIPTION = 'Mark your daily tasks complete/incomplete'

    def _call(self, bot, update, **kwargs):
        if not kwargs['args']:
            update.message.reply_text('Task name is required.')
            return

        ok = mongo.daily_tasks.toggle_task(
            update.message.chat.id,
            kwargs['args'][0],
        )
        if not ok:
            update.message.reply_text('Task was not found')
            return

        update.message.reply_text('Task toggled')
        return True

    def _callback_query_execute(self, bot, update, **kwargs):
        from bot.commands.daily_tasks import common

        mongo.daily_tasks.toggle_task(
            update.callback_query.message.chat.id,
            update.callback_query.data.split()[1],
        )

        update.callback_query.message.edit_text(
            text=common.get_tasks_list_text(),
            reply_markup=InlineKeyboardMarkup(common.get_tasks_markup(update.callback_query.message.chat.id)),
        )
        return True
