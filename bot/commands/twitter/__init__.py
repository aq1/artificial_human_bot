from .list_twitter_accounts import ListTwitterAccountsCommand
from .add_twitter_account import AddTwitterAccountCommand


def get_commands():
    return [
        ListTwitterAccountsCommand(),
        AddTwitterAccountCommand(),
    ]
