from bot.commands.common.start import StartCommand
from bot.commands.common.help import HelpCommand
from bot.commands.common.bot_ip import BotIPCommand
from bot.commands.common.c import CCommand
from bot.commands.common.my_chat_id import MyChatIDCommand
from bot.commands.common.lenny import LennyCommand
from bot.commands.common.shruggie import ShruggieCommand
from bot.commands.common.shame import ShameCommand
from bot.commands.common.twitter_video import TwitterVideoHandler
from bot.commands.common.emojis import (
    ListEmojis,
    create_emoji_commands,
)


def get_commands():
    return [
               StartCommand(),
               HelpCommand(),
               BotIPCommand(),
               CCommand(),
               MyChatIDCommand(),
               LennyCommand(),
               ShruggieCommand(),
               ListEmojis(),
               ShameCommand(),
               TwitterVideoHandler(),
           ] + create_emoji_commands()
