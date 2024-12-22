import random
import logging
import os
from butter_words import BUTTER_WORDS, SENTENCE_PATTERNS
from gpt_instructions import SYSTEM_PROMPT, GENERATION_PROMPTS
from openai import OpenAI

logger = logging.getLogger(__name__)

class ButterTextGenerator:
    def __init__(self, use_gpt=False):
        self.words = BUTTER_WORDS
        self.patterns = SENTENCE_PATTERNS
        self.use_gpt = use_gpt
        if use_gpt:
            api_key = os.environ.get('OPENAI_API_KEY')
            if not api_key:
                logger.warning("OpenAI API key not found, falling back to basic generation")
                self.use_gpt = False
            else:
                self.client = OpenAI(api_key=api_key)
                # the newest OpenAI model is "gpt-4o-mini" which was released Oct 1, 2024
                self.model = "gpt-4o-mini"
        logger.debug(f"Initialized ButterTextGenerator (GPT: {self.use_gpt}) with {len(self.patterns)} patterns")

    def _generate_with_gpt(self, mode, count):
        try:
            prompt = GENERATION_PROMPTS[mode].format(count=count)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500 if mode == "paragraph" else 200
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"GPT generation error: {str(e)}")
            return None

    def generate_sentence(self):
        if self.use_gpt:
            result = self._generate_with_gpt("sentence", 1)
            if result:
                return result
            logger.warning("GPT generation failed, falling back to basic generation")
            
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
        if self.use_gpt:
            result = self._generate_with_gpt("word", count)
            if result:
                return result
            logger.warning("GPT generation failed, falling back to basic generation")
            
        words = []
        categories = list(self.words.keys())
        for _ in range(count):
            category = random.choice(categories)
            words.append(random.choice(self.words[category]))
        return " ".join(words)

    def generate_sentences(self, count):
        if self.use_gpt:
            result = self._generate_with_gpt("sentence", count)
            if result:
                return result
            logger.warning("GPT generation failed, falling back to basic generation")
        return " ".join([self.generate_sentence() for _ in range(count)])

    def generate_paragraphs(self, count):
        if self.use_gpt:
            result = self._generate_with_gpt("paragraph", count)
            if result:
                return result
            logger.warning("GPT generation failed, falling back to basic generation")
            
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
