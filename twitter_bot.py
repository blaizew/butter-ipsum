import logging
import tweepy
import os
import random # Added for random.randint
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from text_generator import ButterTextGenerator

logger = logging.getLogger(__name__)

class ButterTwitterBot:
    def __init__(self):
        self.text_generator = ButterTextGenerator()
        self.scheduler = BackgroundScheduler()

        # Initialize Twitter client using v2 API
        try:
            self.client = tweepy.Client(
                consumer_key=os.environ['TWITTER_API_KEY'],
                consumer_secret=os.environ['TWITTER_API_SECRET'],
                access_token=os.environ['TWITTER_ACCESS_TOKEN'],
                access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
            )
            logger.info("Twitter client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {str(e)}")
            raise

    def generate_daily_post(self):
        """Generate random number of butter-themed sentences (1-8)"""
        try:
            # Generate random number of sentences between 1 and 8
            num_sentences = random.randint(1, 8)
            text = self.text_generator.generate_sentences(num_sentences)
            return text
        except Exception as e:
            logger.error(f"Error generating daily post: {str(e)}")
            return None

    def split_text_into_tweets(self, text, max_length=275):  # 275 to leave room for thread numbering
        """Split long text into multiple tweets"""
        words = text.split()
        tweets = []
        current_tweet = []
        current_length = 0

        for word in words:
            # +1 for the space between words
            if current_length + len(word) + 1 <= max_length:
                current_tweet.append(word)
                current_length += len(word) + 1
            else:
                tweets.append(' '.join(current_tweet))
                current_tweet = [word]
                current_length = len(word) + 1

        if current_tweet:
            tweets.append(' '.join(current_tweet))

        # Add thread numbering
        total = len(tweets)
        if total > 1:
            tweets = [f"{tweet} ({i+1}/{total})" for i, tweet in enumerate(tweets)]

        return tweets

    def post_to_twitter(self):
        """Post the generated text to Twitter using v2 API, creating a thread if needed"""
        try:
            text = self.generate_daily_post()
            if not text:
                return False

            # Split text into tweet-sized chunks
            tweets = self.split_text_into_tweets(text)

            # Post the first tweet
            response = self.client.create_tweet(text=tweets[0])
            if not response.data:
                logger.error("Failed to post initial tweet")
                return False

            previous_tweet_id = response.data['id']
            logger.info(f"Posted initial tweet with ID: {previous_tweet_id}")

            # Post the rest of the thread if there are more tweets
            for tweet in tweets[1:]:
                response = self.client.create_tweet(
                    text=tweet,
                    in_reply_to_tweet_id=previous_tweet_id
                )
                if not response.data:
                    logger.error("Failed to post thread reply")
                    return False
                previous_tweet_id = response.data['id']
                logger.info(f"Posted thread reply with ID: {previous_tweet_id}")

            return True
        except Exception as e:
            logger.error(f"Error posting to Twitter: {str(e)}")
            return False

    def schedule_daily_posts(self):
        """Schedule daily posts at 9am PT"""
        try:
            # Configure scheduler to use PT timezone
            pt_timezone = timezone('US/Pacific')

            # Schedule job to run at 9am PT
            self.scheduler.add_job(
                self.post_to_twitter,
                'cron',
                hour=9,
                minute=0,
                timezone=pt_timezone
            )

            # Start the scheduler
            self.scheduler.start()
            logger.info("Scheduled daily Twitter posts successfully")
            return True
        except Exception as e:
            logger.error(f"Error scheduling daily posts: {str(e)}")
            return False

def create_twitter_bot():
    """Create and initialize the Twitter bot"""
    try:
        bot = ButterTwitterBot()
        success = bot.schedule_daily_posts()
        return bot if success else None
    except Exception as e:
        logger.error(f"Error creating Twitter bot: {str(e)}")
        return None