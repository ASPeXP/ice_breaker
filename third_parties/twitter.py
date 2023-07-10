import os
from datetime import datetime, timezone

import logging

import tweepy

from dotenv import load_dotenv

load_dotenv("./.env")

logger = logging.getLogger("twitter")
# print(os.getenv('OPENAI_API_KEY'))
# print(os.getenv("TWITTER_API_KEY"))
# print(os.getenv("TWITTER_API_SECRET"))
# print(os.getenv("TWITTER_ACCESS_TOKEN"))
# print(os.getenv("TWITTER_ACCESS_SECRET"))
auth = tweepy.OAuthHandler(
    os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET")
)
auth.set_access_token(
    os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)


def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a twitter user's original tweets (i.e. not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "ur".
    """

    tweets = api.user_timeline(screen_name=username, count=num_tweets)

    tweet_list = []

    for tweet in tweets:
        if "RT @" not in tweet.text and not tweet.text.startswith("@"):
            tweet_dict = {}
            tweet_dict["time_posted"] = str(
                datetime.now(timezone.utc) - tweet.created_at
            )
            tweet_dict["text"] = tweet.text
            tweet_dict[
                "url"
            ] = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
            tweet_list.append(tweet_dict)

    return tweet_list
