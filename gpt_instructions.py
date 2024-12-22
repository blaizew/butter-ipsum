"""
Instructions for GPT-based text generation in Butter Ipsum.
These prompts can be easily modified to adjust the style and tone of generated text.
"""

SYSTEM_PROMPT = """You are a specialized text generator that creates butter-themed lorem ipsum text. 
Your output should be food-industry appropriate, focusing on butter-related terminology and culinary themes.
Keep the text professional and suitable for placeholder use."""

GENERATION_PROMPTS = {
    "paragraph": """Generate {count} paragraph(s) of butter-themed placeholder text. 
Each paragraph should be 4-8 sentences long.
Focus on butter-related terms, cooking processes, and culinary descriptions.
Keep the tone professional and suitable for food industry use.
Only return the generated text, no additional formatting or explanations.""",
    
    "sentence": """Generate {count} sentence(s) of butter-themed placeholder text.
Each sentence should be complete and grammatically correct.
Use butter-related terminology and culinary themes.
Only return the generated text, no additional formatting or explanations.""",
    
    "word": """Generate {count} butter-themed words.
Words should be related to butter, dairy, cooking, or culinary arts.
Separate words with spaces.
Only return the generated text, no additional formatting or explanations."""
}
