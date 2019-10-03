from mongo.client import db


def get_emojis(name=None):
    if not name:
        return db.emojis.find({})
    return db.emojis.find({'_id': name})


def update_emojis(name, emojis):
    db.emojis.update(
        {'_id': name},
        {'emojis': emojis},
        upsert=True,
    )
