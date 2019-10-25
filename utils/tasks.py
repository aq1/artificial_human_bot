import os
import sys

from telegram import ParseMode

from celery import Celery
from celery.schedules import crontab

import settings

# Mongo throws a warning "UserWarning: MongoClient opened before fork."
# So mongo module is imported inside the tasks. But you need this to correct import
sys.path.append(os.getcwd())

app = Celery(
    main='artificial_human_bot',
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, find_projects.s())
    sender.add_periodic_task(crontab(hour=8), reset_daily_tasks.s())
    sender.add_periodic_task(crontab(hour=8), send_info.s())


@app.task
def notify_users_about_new_projects():
    import bot
    import mongo

    _bot = bot.get_bot()
    freelance_update_command = bot.commands.markets.FreelanceUpdateCommand()

    for user in mongo.users.get_all_users():
        projects = mongo.projects.get_new_projects(user['chat_id'])
        if not projects:
            continue

        last_seen_projects = freelance_update_command.get_last_seen_projects(projects)

        _bot.send_message(
            chat_id=user['chat_id'],
            text=freelance_update_command.get_message(projects),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        mongo.users.update_last_seen_projects(user['chat_id'], last_seen_projects)
        return True


@app.task
def find_projects():
    import freelance_markets

    inserted, _ = freelance_markets.find_projects()
    if inserted:
        notify_users_about_new_projects.delay()


@app.task
def reset_daily_tasks():
    import mongo
    mongo.daily_tasks.reset_all_tasks()


@app.task
def send_info():
    import bot

    _bot = bot.get_bot()
    bot_ip_command = bot.commands.info.BotIPCommand()
    poloniex_balance_command = bot.commands.info.PoloniexBalanceCommand()

    for text in (bot_ip_command.success_message, poloniex_balance_command.success_message):
        for chat_id in settings.ADMINS:
            _bot.send_message(
                chat_id=chat_id,
                text=text
            )
