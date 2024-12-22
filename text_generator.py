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
        
        # Initialize OpenAI client if using GPT
        if self.use_gpt:
            try:
                self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
                # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
                # do not change this unless explicitly requested by the user
                self.model = "gpt-4o-mini"
                logger.debug("Initialized OpenAI client")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {str(e)}")
                self.use_gpt = False
                logger.warning("GPT generation failed, falling back to basic generation")
        
        logger.debug(f"Initialized ButterTextGenerator with {len(self.patterns)} patterns")
        logger.debug(f"GPT generation: {'enabled' if self.use_gpt else 'disabled'}")

    def generate_with_gpt(self, count, mode):
        """Generate text using GPT model"""
        try:
            system_prompt = create_system_prompt(self.tuning_params)
            user_prompt = create_user_prompt(count, mode)
            
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
            logger.debug(f"Successfully generated text using GPT")
            return text
        except Exception as e:
            logger.error(f"GPT generation error: {str(e)}")
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
