import json
import random
from collections import defaultdict
from functools import lru_cache

from bot.commands import (
    BaseCommand,
)


@lru_cache()
def get_mark_model(window=1):
    mark = dict()
    with open('settings/parsed_messages.json', 'r', encoding='utf8') as f:
        all_messages = json.load(f)
    
    for user_id, messages in all_messages.items():
        user_id = int(user_id)
        for i in range(window, len(messages) - window, window):
            mark[user_id] = defaultdict(lambda: defaultdict(int))
            mark[user_id][tuple(messages[i - window:i])][messages[i]] += 1
            
    return mark


class MarkCommand(BaseCommand):

    _COMMAND = 'mark'
    _DESCRIPTION = 'Generate message'

    def _call(self, bot, update, **kwargs):
        try:
            user_id = kwargs['args'][0]
            mark_window = int(kwargs['args'][1])
            length = int(kwargs['args'][2])
        except (KeyError, IndexError):
            user_id = update.message.chat.id
            mark_window = 1
            length = 20
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
            if word == '.':
                break
            key = tuple(sentence[-mark_window:])
    
        sentence = ' '.join(sentence).capitalize().replace(' .', '.')
        bot.send_message(
            update.message.chat.id,
            text=sentence,
        )
        return True
