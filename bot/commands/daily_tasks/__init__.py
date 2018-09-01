import telegram.ext

from bot.commands.daily_tasks.add_daily_task import AddDailyTaskCommand
from bot.commands.daily_tasks.remove_daily_task import RemoveDailyTaskCommand
from bot.commands.daily_tasks.toggle_daily_task import ToggleDailyTaskCommand
from bot.commands.daily_tasks.get_daily_tasks import GetDailyTasksCommand


def get_commands():
    return [
        AddDailyTaskCommand(pass_args=True),
        RemoveDailyTaskCommand(pass_args=True),
        ToggleDailyTaskCommand(pass_args=True),
        GetDailyTasksCommand(),
    ]


def get_callback_queries():
    return [
        telegram.ext.CallbackQueryHandler(
            RemoveDailyTaskCommand(),
            pattern='{} .+'.format(RemoveDailyTaskCommand.get_command()),
        ),
        telegram.ext.CallbackQueryHandler(
            ToggleDailyTaskCommand(),
            pattern='{} .+'.format(ToggleDailyTaskCommand.get_command()),
        ),
    ]
