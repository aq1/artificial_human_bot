import sys

import bot
import tasks


if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = 'start_bot'

    if arg == 'start_bot':
        bot.start_bot()
    if arg == 'find_projects':
        tasks.find_projects()
