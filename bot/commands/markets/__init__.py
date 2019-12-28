from bot.commands.markets.freelance_updates import FreelanceUpdateCommand
from bot.commands.markets.get_queries import GetQueriesCommand
from bot.commands.markets.add_query import AddQueryCommand
from bot.commands.markets.remove_query import RemoveQueryCommand


def get_commands():
    return [
        FreelanceUpdateCommand(),
        GetQueriesCommand(),
        AddQueryCommand(),
        RemoveQueryCommand(),
    ]
