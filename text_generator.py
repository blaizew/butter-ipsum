import random
import logging
import os
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

                logger.debug("Initializing OpenAI client...")
                self.openai_client = OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized successfully")

            except ValueError as ve:
                logger.error(f"Configuration error: {str(ve)}")
                self.use_gpt = False
            except Exception as e:
                logger.error(f"Unexpected error initializing OpenAI client: {str(e)}")
                self.use_gpt = False

        logger.debug(f"Initialized ButterTextGenerator with {len(self.patterns)} patterns")
        logger.debug(f"GPT generation: {'enabled' if self.use_gpt else 'disabled'}")
        if self.use_gpt:
            logger.debug(f"Using model: {self.model}")

    def generate_twitter_post(self):
        """Generate a Twitter-friendly post (within 280 characters)"""
        try:
            # Generate 2-3 sentences for Twitter
            num_sentences = random.randint(2, 3)
            sentences = []
            total_length = 0

            for _ in range(num_sentences):
                sentence = self.generate_sentence()
                # Check if adding this sentence would exceed Twitter's limit
                if total_length + len(sentence) + 1 > 280:  # +1 for space
                    break
                sentences.append(sentence)
                total_length += len(sentence) + 1  # +1 for space

            text = " ".join(sentences)
            logger.debug(f"Generated Twitter post: {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error generating Twitter post: {str(e)}")
            return None

    def generate_with_gpt(self, count, mode):
        """Generate text using GPT model"""
        if not self.openai_client:
            logger.warning("OpenAI client not initialized")
            raise ValueError("GPT generation is not available - OpenAI client not initialized")

        try:
            logger.debug(f"Preparing GPT generation for {count} {mode}(s)")
            system_prompt = create_system_prompt(self.tuning_params)
            user_prompt = create_user_prompt(count, mode)

            logger.debug(f"Sending request to OpenAI API using model {self.model}")
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
            logger.info(f"Successfully generated text using GPT ({len(text)} chars)")
            return text

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error during GPT text generation: {error_msg}")
            if "insufficient_quota" in str(e):
                raise ValueError("OpenAI API quota exceeded. Please try again later.")
            elif "rate_limit" in str(e):
                raise ValueError("OpenAI API rate limit reached. Please try again in a few moments.")
            else:
                raise ValueError(f"GPT generation failed: {str(e)}")

    def generate_sentence(self):
        """Generate a single sentence"""
        if self.use_gpt:
            return self.generate_with_gpt(1, "sentence")

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
            return self.generate_with_gpt(count, "word")

        words = []
        categories = list(self.words.keys())
        for _ in range(count):
            category = random.choice(categories)
            words.append(random.choice(self.words[category]))
        return " ".join(words)

    def generate_sentences(self, count):
        """Generate multiple sentences"""
        if self.use_gpt:
            return self.generate_with_gpt(count, "sentence")

        return " ".join([self.generate_sentence() for _ in range(count)])

    def generate_paragraphs(self, count):
        """Generate multiple paragraphs"""
        if self.use_gpt:
            return self.generate_with_gpt(count, "paragraph")

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