import random
import logging
import os
import time
from openai import OpenAI
from butter_words import BUTTER_WORDS, SENTENCE_PATTERNS
from gpt_prompts import create_system_prompt, create_user_prompt, DEFAULT_TUNING_PARAMS

logger = logging.getLogger(__name__)

class ButterTextGenerator:
    def __init__(self, use_gpt=False, tuning_params=None):
        self.words = BUTTER_WORDS
        self.patterns = SENTENCE_PATTERNS
        self.use_gpt = use_gpt
        self.tuning_params = tuning_params or DEFAULT_TUNING_PARAMS
        self.openai_client = None
        self.model = "gpt-4o-mini"  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        
        logger.debug(f"Initializing ButterTextGenerator (GPT: {use_gpt})")
        
        # Initialize OpenAI client if using GPT
        if self.use_gpt:
            try:
                api_key = os.environ.get("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OpenAI API key not found in environment variables")
                
                logger.debug("Attempting to initialize OpenAI client...")
                self.openai_client = OpenAI(api_key=api_key)
                
                # Skip initial validation if we're in a rate-limited state
                if hasattr(self.__class__, '_rate_limited_until') and \
                   self.__class__._rate_limited_until > time.time():
                    logger.warning("Skipping initial validation due to rate limiting")
                    return
                
                # Validate API key with a minimal request
                try:
                    response = self.openai_client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": "test"}],
                        max_tokens=1
                    )
                    if response:
                        logger.info("OpenAI client successfully initialized and tested")
                except Exception as e:
                    if "rate_limit" in str(e).lower() or "429" in str(e):
                        # Set a class-level rate limit timeout (5 minutes)
                        self.__class__._rate_limited_until = time.time() + 300
                        logger.warning("Rate limited. Will retry after 5 minutes.")
                        self.use_gpt = False
                        return
                    raise  # Re-raise other exceptions
                
            except ValueError as ve:
                logger.error(str(ve))
                self.use_gpt = False
            except Exception as e:
                error_msg = str(e)
                if "invalid_api_key" in error_msg.lower():
                    logger.error("Invalid OpenAI API key provided")
                elif "insufficient_quota" in error_msg.lower():
                    logger.error("OpenAI API quota exceeded")
                elif "rate_limit" in error_msg.lower() or "429" in error_msg:
                    # Set a class-level rate limit timeout (5 minutes)
                    self.__class__._rate_limited_until = time.time() + 300
                    logger.warning("Rate limited. Will retry after 5 minutes.")
                else:
                    logger.error(f"Error initializing OpenAI client: {error_msg}")
                self.use_gpt = False
        
        logger.debug(f"Initialized ButterTextGenerator with {len(self.patterns)} patterns")
        logger.debug(f"GPT generation: {'enabled' if self.use_gpt else 'disabled'}")
        if self.use_gpt:
            logger.debug(f"Using model: {self.model}")

    def generate_with_gpt(self, count, mode):
        """Generate text using GPT model"""
        if not self.openai_client:
            logger.warning("OpenAI client not initialized, falling back to basic generation")
            return None

        # Check if we're currently rate limited
        if hasattr(self.__class__, '_rate_limited_until'):
            if time.time() < self.__class__._rate_limited_until:
                remaining_time = int(self.__class__._rate_limited_until - time.time())
                logger.warning(f"Rate limit cooldown: {remaining_time} seconds remaining")
                return None
            else:
                # Reset rate limiting if cooldown period has passed
                delattr(self.__class__, '_rate_limited_until')

        try:
            logger.debug(f"Preparing GPT generation for {count} {mode}(s)")
            system_prompt = create_system_prompt(self.tuning_params)
            user_prompt = create_user_prompt(count, mode)
            
            logger.debug("Sending request to OpenAI API")
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=200 if mode == 'word' else 500 if mode == 'sentence' else 1000,
                temperature=0.8
            )
            
            text = response.choices[0].message.content
            logger.debug(f"Successfully generated text using GPT: {len(text)} characters")
            return text
        except Exception as e:
            error_msg = str(e)
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                # Set a class-level rate limit timeout (5 minutes)
                self.__class__._rate_limited_until = time.time() + 300
                logger.warning("Rate limited. Will retry after 5 minutes.")
            elif "insufficient_quota" in error_msg:
                logger.error("OpenAI API quota exceeded")
                self.use_gpt = False  # Permanently disable GPT for quota issues
            else:
                logger.error(f"GPT generation error: {error_msg}")
            
            logger.warning("GPT generation failed, falling back to basic generation")
            return None

    def generate_sentence(self):
        """Generate a single sentence"""
        if self.use_gpt:
            gpt_text = self.generate_with_gpt(1, "sentence")
            if gpt_text:
                return gpt_text
        
        try:
            pattern = random.choice(self.patterns)
            logger.debug(f"Selected pattern: {pattern}")
            
            sentence = pattern.format(
                adj=random.choice(self.words['adjectives']),
                nouns=random.choice(self.words['nouns']),
                verbs=random.choice(self.words['verbs']),
                descriptions=random.choice(self.words['descriptions'])
            )
            # Ensure proper capitalization
            return sentence[0].upper() + sentence[1:]
        except KeyError as e:
            logger.error(f"Missing word category: {str(e)}")
            return "Error generating sentence: missing word category"
        except Exception as e:
            logger.error(f"Error generating sentence: {str(e)}")
            return "Error generating sentence"

    def generate_words(self, count):
        """Generate a list of words"""
        if self.use_gpt:
            gpt_text = self.generate_with_gpt(count, "word")
            if gpt_text:
                return gpt_text
        
        words = []
        categories = list(self.words.keys())
        for _ in range(count):
            category = random.choice(categories)
            words.append(random.choice(self.words[category]))
        return " ".join(words)

    def generate_sentences(self, count):
        """Generate multiple sentences"""
        if self.use_gpt:
            gpt_text = self.generate_with_gpt(count, "sentence")
            if gpt_text:
                return gpt_text
        
        return " ".join([self.generate_sentence() for _ in range(count)])

    def generate_paragraphs(self, count):
        """Generate multiple paragraphs"""
        if self.use_gpt:
            gpt_text = self.generate_with_gpt(count, "paragraph")
            if gpt_text:
                return gpt_text
        
        try:
            paragraphs = []
            for _ in range(count):
                # Generate 4-8 sentences per paragraph
                num_sentences = random.randint(4, 8)
                paragraph = self.generate_sentences(num_sentences)
                paragraphs.append(paragraph)
            logger.debug(f"Generated {count} paragraphs")
            return "\n\n".join(paragraphs)
        except Exception as e:
            logger.error(f"Error generating paragraphs: {str(e)}")
            return "Error generating paragraphs"
