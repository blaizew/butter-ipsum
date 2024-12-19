import random
from butter_words import BUTTER_WORDS, SENTENCE_PATTERNS

class ButterTextGenerator:
    def __init__(self):
        self.words = BUTTER_WORDS
        self.patterns = SENTENCE_PATTERNS

    def generate_sentence(self):
        pattern = random.choice(self.patterns)
        sentence = pattern.format(
            adj=random.choice(self.words['adjectives']),
            noun=random.choice(self.words['nouns']),
            verb=random.choice(self.words['verbs']),
            adv=random.choice(self.words['adverbs'])
        )
        # Capitalize first letter and add period
        return sentence[0].upper() + sentence[1:] + "."

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
        paragraphs = []
        for _ in range(count):
            # Generate 4-8 sentences per paragraph
            num_sentences = random.randint(4, 8)
            paragraph = self.generate_sentences(num_sentences)
            paragraphs.append(paragraph)
        return "\n\n".join(paragraphs)
