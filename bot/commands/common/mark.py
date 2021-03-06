import os
import json
import random
from collections import defaultdict
from functools import lru_cache

import settings
from bot.commands import (
    BaseCommand,
)


@lru_cache()
def get_mark_model(window=1):
    mark = dict()
    with open(os.path.join(settings.BASE_DIR, 'settings', 'parsed_messages.json'), 'r', encoding='utf8') as f:
        all_messages = json.load(f)
    
    for user_id, messages in all_messages.items():
        user_id = int(user_id)
        mark[user_id] = defaultdict(lambda: defaultdict(int))
        for i in range(window, len(messages) - window, window):
            mark[user_id][tuple(messages[i - window:i])][messages[i]] += 1
            
    return mark


class MarkCommand(BaseCommand):

    _COMMAND = 'mark'
    _DESCRIPTION = 'Generate message'

    def _call(self, update, context):
        try:
            mark_window = int(context.args[0])
            length = int(context.args[1])
            user_id = context.args[2]
        except (KeyError, IndexError):
            mark_window = 2
            length = 50
            user_id = update.message.from_user.id
        except ValueError:
            update.message.reply_text('Bad arguments')
            return 

        mark = get_mark_model(mark_window).get(user_id)
        if not mark:
            update.message.reply_text('No messages for this user')
            return

        key = random.choice(list(mark.keys()))
        sentence = [k for k in key]
    
        for x in range(length):
            choices, weights, total = [], [], sum(mark[key].values())
            for k, v in mark[key].items():
                choices.append(k)
                weights.append(v / total)
            try:
                word = random.choices(
                    population=choices,
                    weights=weights,
                    k=1,
                )[0]
            except IndexError:
                break
            sentence.append(word)
            key = tuple(sentence[-mark_window:])
    
        sentence = ' '.join(sentence).capitalize()
        context.bot.send_message(
            update.message.chat.id,
            text=sentence,
        )
        return True
