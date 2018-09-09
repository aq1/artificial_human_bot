from bot.commands.storage.list_storage import ListStorageCommand
from bot.commands.storage.save import SaveCommand


def get_commands():
    return [
        ListStorageCommand(),
        SaveCommand(pass_args=True),
    ]
