import tweepy

import settings
from bot.commands.base import BaseRegexHandler


class TwitterVideoHandler(BaseRegexHandler):

    REGEX = r'^.*?twitter\.com.*?status\/.*?$'

    def _callback(self, update, context):

        try:
            tweet_id = update.message.text.split('status')[-1].strip('/')
        except ValueError:
            return

        if not tweet_id:
            return

        auth = tweepy.OAuthHandler(
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_REDIRECT_URI,
        )
        api = tweepy.API(auth)
        status = api.get_status(tweet_id)
        video = max(
            status._json['extended_entities']['media'][0]['video_info']['variants'],
            key=lambda v: v.get('bitrate', 0),
        )

        try:
            context.bot.send_message(update.message.chat_id, video['url'])
        except KeyError:
            return
