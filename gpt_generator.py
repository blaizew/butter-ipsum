import os
import logging
from openai import OpenAI
from gpt_instructions import SYSTEM_PROMPT, GENERATION_PROMPTS

logger = logging.getLogger(__name__)

class GPTTextGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o-mini"
        logger.debug("Initialized GPTTextGenerator")

    def generate_text(self, count, mode):
        """Generate text using OpenAI's GPT model."""
        try:
            prompt = GENERATION_PROMPTS[mode].format(count=count)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000 if mode == "paragraph" else 500
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating text with GPT: {str(e)}")
            return f"Error generating text: {str(e)}"
