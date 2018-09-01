from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot.commands import BaseCommand
from bot.commands.daily_tasks import (
    RemoveDailyTaskCommand,
    MarkDailyTaskCommand,
)

import mongo


class GetDailyTasksCommand(BaseCommand):

    _COMMAND = 'get_daily_tasks'
    _DESCRIPTION = 'Get your daily tasks'

    def _call(self, bot, update, **kwargs):
        tasks = mongo.daily_tasks.get_tasks(update.message.chat.id)

        if not tasks:
            update.message.reply_text('You have no daily tasks')
            return

        reply_markup = [
            [InlineKeyboardButton(t['name'], callback_data='{} {}'.format(MarkDailyTaskCommand.get_command(), t['name'])),
             InlineKeyboardButton('🗑', callback_data='{} {}'.format(RemoveDailyTaskCommand.get_command(), t['name']))]
            for t in tasks
        ]

        update.message.reply_text(
            text=(
                'Your daily tasks.\n'
                'Click name to mark task complete / incomplete.\n'
                '✅ means task is complete\n'
                '🗑 to remove task'
            ),
            reply_markup=InlineKeyboardMarkup(reply_markup),
            disable_web_page_preview=True,
        )
        return True
