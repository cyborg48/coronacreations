import tweepy
import logging
from config import create_api
import json
import time
import toneanalyzer
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# https://twitter.com/<user_displayname>/status/<tweet_id>
artkeys = ["watercolor", "acrylic paint", "oil paint", "gouache", "oil pastel", "colored pencil", "mixed media", "i sketched",
            "digital painting", "digital art", "chalk pastel", "my poem", "my painting", "arts and crafts", 
            "i painted", "digital art", "krita", "medibang", "clip studio paint", "escapril", "creative writing" "lineart", "micron", "prismacolor",
            "i wrote a poem", "i wrote a story", "i wrote a song"]

exclude = ["sale", "shop", "buy", "% off", "vent", "nsfw", "shit", "fuck", "bitch", "nude"]

indicators = ["i'm scared", "i'm worried", "i'm stressed", "i'm upset", "i'm terrified"]

covid_indicators = ["coronavirus", "virus" "corona virus", "pandemic", "covid", "quarantine", "lockdown", "lock down", "isolat", "test positive", "tested positive", "social distanc"]

retweeted_ids = []


class RetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                # print(tweet.user)

                containsKey = False

                for phrase in artkeys:
                    if phrase in tweet.text.lower():
                        containsKey = True
                for phrase in exclude:
                    if phrase in tweet.text.lower():
                        containsKey = False
                # print(containsKey, 'media' in tweet.entities, not hasattr(tweet, 'retweeted_status'), not tweet.possibly_sensitive, tweet.user.followers_count < 5000)
                if(containsKey and 'media' in tweet.entities and not hasattr(tweet, 'retweeted_status') and not tweet.possibly_sensitive and tweet.user.followers_count < 5000 and tweet.user.followers_count > 50):

                    # print(tweet.possibly_sensitive)
                    print("Meets criteria")

                    global retweeted_ids

                    getTweet = tweepy.Cursor(self.api.search, q="i'm%20scared OR i'm%20worried OR i'm%20stressed OR i'm%20upset OR i'm%20anxious OR \
                            i'm%20terrified", result_type = "recent", lang='en').items(5000)
                    # cutoff = random.randint(0, 5000)
                    # getTweet = getTweet[cutoff:]
                    # getTweet = getTweet[0][cutoff:]
                    # print(getTweet[0][0])
                    # print(len(getTweet))

                    tweeted = False

                    count = 0

                    for replyTweet in getTweet:

                        # print(count)

                        if not replyTweet.id in retweeted_ids and not tweeted and not hasattr(replyTweet, 'retweeted_status'):
                        
                            afraid = False
                            abtCovid = False
                            
                            for phrase in covid_indicators:
                                if phrase in replyTweet.text.lower():
                                    abtCovid = True
                                    print("true1")

                            for phrase in indicators:
                                if phrase in replyTweet.text.lower():
                                    afraid = True
                                    print("true2")

                            # tones = toneanalyzer.analyze(replyTweet.text)
                            # print(tones)
                        
                            # if(("fear" in tones or "joy" in tones) and not 'joy' in tones and not 'anger' in tones):
                            if abtCovid:
                                newTweet = "https://twitter.com/" + replyTweet.user.screen_name + "/status/" + str(replyTweet.id) + \
                                    " I wish I could do more to ease your fears right now. Alas, I am only a few lines of code "\
                                    "but I hope this piece brings you some comfort and solidarity. Please know that you are not alone. " + \
                                     "https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id)
                        
                                self.api.update_status(newTweet)
                                print("Retweeted")
                                # retweeted_ids.append(replyTweet.id)
                                # if(len(retweeted_ids) > 100):
                                #     retweeted_ids = retweeted_ids[80:]
                                # for id in retweeted_ids:
                                #    print(id)
                                tweeted = True
                                time.sleep(5)
                        count += 1

            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

def main():

    #artkeys = ["watercolor", "acrylic paint", "oil paint", "gouache", "oil pastel", "colored pencil", "graphite", "mixed media", "my poetry",
    #        "digital painting", "digital art", "chalk pastel", "my writing", "my poem", "my painting", "my art"]
    #covidkeys = ["coronavirus", "corona", "virus", "covid19", "stressed", "worried", "scared"]

    api = create_api()

    retweets_listener = RetweetListener(api)
    artstream = tweepy.Stream(api.auth, retweets_listener)
    artstream.filter(track=artkeys, languages=["en"], is_async=True)
    
    '''
    while(True):

        if(tweet1 != None and tweet2 != None):

            if(not(tweet1.retweeted) or not(tweet2.retweeted)):

                    newTweet = "https://twitter.com/" + tweet1.user.screen_name + "/status/" + tweet1.id, \
                            "@" + tweet1.user.screen_name,\
                            "I wish I could do more to ease your stress about #covid19. Alas, I am only a few lines of code "\
                            "but I hope this piece by @" + tweet2.user.screen_name + " brings you some comfort!",\
                             "https://twitter.com/" + tweet2.user.screen_name + "/status/" + tweet2.id
                    
                    api.update_status(newTweet)
                    '''

if __name__ == "__main__":
    main()
