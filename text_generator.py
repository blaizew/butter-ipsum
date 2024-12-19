import random
import logging
from butter_words import BUTTER_WORDS, SENTENCE_PATTERNS

logger = logging.getLogger(__name__)

class ButterTextGenerator:
    def __init__(self):
        self.words = BUTTER_WORDS
        self.patterns = SENTENCE_PATTERNS
        logger.debug(f"Initialized ButterTextGenerator with {len(self.patterns)} patterns")

    def generate_sentence(self):
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
        words = []
        categories = list(self.words.keys())
        for _ in range(count):
            category = random.choice(categories)
            words.append(random.choice(self.words[category]))
        return " ".join(words)

    def generate_sentences(self, count):
        return " ".join([self.generate_sentence() for _ in range(count)])

    def generate_paragraphs(self, count):
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
