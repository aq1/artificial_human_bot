from bot.commands import (
    AdminBaseCommand,
)

from mongo import twitter


class ListTwitterAccountsCommand(AdminBaseCommand):

    _COMMAND = 'list_twitter_accounts'

    @property
    def success_message(self):
        accounts = twitter.get_twitter_accounts()
        return '\n\n'.join([a['username'] for a in accounts])
