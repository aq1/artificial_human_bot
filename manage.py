import os

import settings
import bot


if __name__ == '__main__':
    pid_path = os.path.join(settings.PID_PATH)
    with open(pid_path, 'w') as f:
        f.write(str(os.getpid()))
    bot.start_bot()
