from typing import Any, Dict, List
import tweepy
from src.connection import trends_collection
from src.secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from src.constants import BRAZIL_WOE_ID


def _get_trends(woe_id: int, api: tweepy.API) -> List[Dict[str, Any]]:
    # Get trends in the Twitter
    trends = api.trends_place(woe_id)

    return trends[0]["trends"]


def get_trends_from_mongo() -> List[Dict[str, Any]]:
    trends = trends_collection.find({})
    return list(trends)


def trends_save() -> None:
    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    trends = _get_trends(BRAZIL_WOE_ID, api)
    trends_collection.insert_many(trends)
