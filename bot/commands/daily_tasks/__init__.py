from bot.commands.daily_tasks.add_daily_task import AddDailyTaskCommand
from bot.commands.daily_tasks.remove_daily_task import RemoveDailyTaskCommand
from bot.commands.daily_tasks.mark_daily_task import MarkDailyTaskCommand
from bot.commands.daily_tasks.get_daily_tasks import GetDailyTasksCommand


def get_commands():
    return [
        AddDailyTaskCommand(pass_args=True),
        RemoveDailyTaskCommand(pass_args=True),
        MarkDailyTaskCommand(pass_args=True),
        GetDailyTasksCommand(),
    ]
