from telegram import InlineKeyboardMarkup

from bot.commands import BaseCommand
from bot.commands.daily_tasks import common


class GetDailyTasksCommand(BaseCommand):

    _COMMAND = 'get_daily_tasks'
    _DESCRIPTION = 'Get your daily tasks'

    def _call(self, bot, update, **kwargs):
        reply_markup = common.get_tasks_markup(update.message.chat.id)

        if not reply_markup:
            update.message.reply_text('You have no daily tasks')
            return

        update.message.reply_text(
            text=common.get_tasks_list_text(),
            reply_markup=InlineKeyboardMarkup(reply_markup),
            disable_web_page_preview=True,
        )
        return True
