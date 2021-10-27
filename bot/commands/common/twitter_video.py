import tweepy

import settings
from bot.commands.base import BaseRegexHandler


class TwitterVideoHandler(BaseRegexHandler):

    REGEX = r'^.*?twitter\.com.*?status\/.*?$'
    _DESCRIPTION = 'Extract video from twitter link'

    def _callback(self, update, context):

        def failed(msg):
            context.bot.send_message(update.message.chat_id, msg)

        try:
            tweet_id = update.message.text.split('status')[-1].strip('/')
        except ValueError:
            return failed('Could not get tweet id')

        if not tweet_id:
            return

        auth = tweepy.OAuthHandler(
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_REDIRECT_URI,
        )
        api = tweepy.API(auth)
        status = api.get_status(tweet_id)
        try:
            video = max(
                status._json['extended_entities']['media'][0]['video_info']['variants'],
                key=lambda v: v.get('bitrate', 0),
            )
        except (KeyError, IndexError):
            return failed('Could not find entities')

        try:
            context.bot.send_message(update.message.chat_id, video['url'])
        except KeyError:
            return failed('Could not find video url')
