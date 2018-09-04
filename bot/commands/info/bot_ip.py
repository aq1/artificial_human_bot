import requests

from bot.commands import (
    AdminBaseCommand,
)


class BotIPCommand(AdminBaseCommand):

    _COMMAND = 'bot_ip'

    @property
    def success_message(self):
        try:
            ip = requests.get('https://api.ipify.org?format=json').json()['ip']
        except (requests.HTTPError, ValueError, TypeError) as e:
            return 'Failed to get IP {}'.format(e)

        return str(ip)
