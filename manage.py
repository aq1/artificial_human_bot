import os
import sys

import settings
import bot
import tasks


if __name__ == '__main__':
    pid_path = os.path.join(settings.PID_PATH)
    with open(pid_path, 'w') as f:
        f.write(str(os.getpid()))

    try:
        arg = sys.argv[1]
    except IndexError:
        arg = 'start_bot'

    if arg == 'start_bot':
        bot.start_bot()
    if arg == 'find_projects':
        tasks.find_projects()
