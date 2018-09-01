from pymongo.errors import DuplicateKeyError

from mongo.client import db


def add_task(chat_id, name):
    try:
        db.daily_tasks.insert_one({
            'chat_id': chat_id,
            'name': name,
            'done': False,
        })
    except DuplicateKeyError:
        return False
    return True


def remove_task(chat_id, name):
    task = get_task(chat_id, name)
    if not task:
        return

    db.daily_tasks.remove(task)
    return True


def get_task(chat_id, name):
    return db.daily_tasks.find_one({
        'chat_id': chat_id,
        'name': name,
    })


def get_tasks(chat_id):
    return db.daily_tasks.find({
        'chat_id': chat_id,
    })


def set_task_done(chat_id, name):
    db.daily_tasks.update(
        {'chat_id': chat_id, 'name': name},
        {'$set': {'done': True}}
    )


def reset_all_tasks():
    db.daily_tasks.update(
        {},
        {'$set': {'done': False}},
        multi=True,
    )
