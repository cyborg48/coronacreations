import tweepy
import logging
import os
import keys

logger = logging.getLogger()

def create_api():
    consumer_key = keys.consumer_key
    consumer_secret = keys.consumer_key_secret 
    access_token = keys.access_token 
    access_token_secret = keys.access_token_secret 

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

