from telegram import InlineKeyboardButton

import mongo

from bot.commands.daily_tasks import (
    RemoveDailyTaskCommand,
    ToggleDailyTaskCommand,
)


def get_tasks_markup(chat_id):
    tasks = mongo.daily_tasks.get_tasks(chat_id)

    reply_markup = []
    for task in tasks:
        toggle_callback = '{} {}'.format(ToggleDailyTaskCommand.get_command(), task['name'])
        remove_callback = '{} {}'.format(RemoveDailyTaskCommand.get_command(), task['name'])
        name = task['name']
        if task['done']:
            name = '✅ {}'.format(name)
        reply_markup.append([
            InlineKeyboardButton(name, callback_data=toggle_callback),
            InlineKeyboardButton('🗑', callback_data=remove_callback)
        ])

    return reply_markup


def get_tasks_list_text():
    return (
        'Your daily tasks.\n'
        'Click name to mark task complete / incomplete.\n'
        '✅ means task is complete\n'
        '🗑 to remove task'
    )
