import logging
import tweepy
import os
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
        except KeyError as e:
            logger.error(f"Missing environment variable: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {str(e)}")
            raise

    def generate_daily_post(self):
        """Generate a single paragraph of butter-themed text"""
        try:
            # Generate one paragraph of butter-themed text
            text = self.text_generator.generate_paragraphs(1)
            logger.debug(f"Generated text for daily post (length: {len(text)})")
            return text
        except Exception as e:
            logger.error(f"Error generating daily post: {str(e)}")
            return None

    def post_to_twitter(self):
        """Post the generated text to Twitter using v2 API"""
        try:
            text = self.generate_daily_post()
            if not text:
                logger.error("Failed to generate text for tweet")
                return False

            logger.debug(f"Attempting to post tweet with length: {len(text)} characters")
            logger.debug(f"Tweet text preview: {text[:100]}...")

            try:
                response = self.client.create_tweet(text=text)
            except tweepy.TweepyException as te:
                if '403' in str(te):
                    logger.error(f"Twitter API 403 Forbidden error. Please verify API keys and permissions. Error: {str(te)}")
                    return False
                elif '401' in str(te):
                    logger.error(f"Twitter API 401 Unauthorized error. Please verify API credentials. Error: {str(te)}")
                    return False
                else:
                    logger.error(f"Twitter API error: {str(te)}")
                    return False

            if not response.data:
                logger.error("Failed to post tweet: No response data")
                return False

            tweet_id = response.data['id']
            logger.info(f"Successfully posted tweet with ID: {tweet_id}")
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