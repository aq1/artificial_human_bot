from mongo.client import db


def get_twitter_accounts(name=None):
    if name:
        return db.twitter.find_one({'_id': name})
    return db.twitter.find({})


def update_twitter_account(name, data):
    db.twitter.update(
        {'_id': name},
        data,
        upsert=True,
    )
