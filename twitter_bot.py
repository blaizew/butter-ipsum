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
        except Exception as e:
            logger.error(f"Failed to initialize Twitter client: {str(e)}")
            raise

    def generate_daily_post(self):
        """Generate a single paragraph of butter-themed text"""
        try:
            # Generate one paragraph of butter-themed text
            text = self.text_generator.generate_paragraphs(1)

            # Ensure the text fits Twitter's character limit (280 chars)
            if len(text) > 280:
                # If too long, generate sentences instead
                text = self.text_generator.generate_sentences(2)
                if len(text) > 280:
                    # If still too long, generate a single sentence
                    text = self.text_generator.generate_sentences(1)

            return text
        except Exception as e:
            logger.error(f"Error generating daily post: {str(e)}")
            return None

    def post_to_twitter(self):
        """Post the generated text to Twitter using v2 API"""
        try:
            text = self.generate_daily_post()
            if text:
                # Use v2 create_tweet endpoint
                response = self.client.create_tweet(text=text)
                if response.data:
                    logger.info(f"Successfully posted tweet with ID: {response.data['id']}")
                    return True
                else:
                    logger.error("Failed to post tweet: No response data")
                    return False
            return False
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