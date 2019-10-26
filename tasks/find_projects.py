from telegram import ParseMode

import mongo
import bot
import freelance_markets


def notify_users_about_new_projects():

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
            disable_notification=True,
        )
        mongo.users.update_last_seen_projects(user['chat_id'], last_seen_projects)
        return True


def find_projects():
    inserted, _ = freelance_markets.find_projects()
    if inserted:
        notify_users_about_new_projects()


if __name__ == '__main__':
    find_projects()
