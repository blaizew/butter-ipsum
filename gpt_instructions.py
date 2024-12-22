"""
Instructions for GPT-4o model to generate butter-themed lorem ipsum text.
These can be easily modified to adjust the style and tone of generated text.
"""

SYSTEM_PROMPT = """You are a specialized text generator that creates butter-themed placeholder text.
Your output should be creative, food-focused, and maintain a consistent butter theme throughout.
Generate text that captures the essence of butter while being suitable for placeholder content."""

GENERATION_PROMPTS = {
    "paragraph": """Generate {count} paragraph(s) of butter-themed text. Each paragraph should:
- Be 4-8 sentences long
- Focus on butter-related themes (cooking, baking, texture, flavor)
- Use varied sentence structures
- Maintain a professional yet creative tone
- Be suitable for use as placeholder text""",
    
    "sentence": """Generate {count} distinct sentence(s) about butter. Each sentence should:
- Be complete and grammatically correct
- Focus on different aspects of butter (taste, cooking, history, etc.)
- Vary in length and structure
- Be suitable for use as placeholder text""",
    
    "word": """Generate {count} distinct butter-related word(s). The words should:
- Be related to butter, dairy, cooking, or baking
- Include a mix of nouns, adjectives, and verbs
- Be suitable for use in food-related content
Return only the words, separated by spaces."""
}
