"""
GPT prompt templates and utilities for text generation
"""

DEFAULT_TUNING_PARAMS = {
    "playfulness": 7,  # 1-10: How playful and whimsical the text should be
    "humor": 4,        # 1-10: Level of humor and wit
    "emotion": 6,      # 1-10: Emotional depth and expressiveness
    "poetic": 8,       # 1-10: Poetic and artistic quality
    "metaphorical": 8, # 1-10: Use of metaphors and analogies
    "technical": 3,    # 1-10: Technical detail and complexity
}

def create_system_prompt(tuning_params=None):
    """Create a system prompt based on tuning parameters"""
    if tuning_params is None:
        tuning_params = DEFAULT_TUNING_PARAMS
    
    # Normalize parameters to 0-1 range for clearer instruction
    params = {k: v/10 for k, v in tuning_params.items()}
    
    return f"""You are a specialized text generator that creates butter-themed placeholder text.
Your output should be creative, food-focused, and maintain a consistent butter theme throughout.
Generate text that captures the essence of butter while being suitable for placeholder content.

Style Guidelines (adjusted by parameters):
- Playfulness: {params['playfulness']:.1f} - {'Very playful and whimsical' if params['playfulness'] > 0.7 else 'Moderately playful' if params['playfulness'] > 0.3 else 'More serious and straightforward'}
- Humor: {params['humor']:.1f} - {'Incorporate witty elements and humor' if params['humor'] > 0.7 else 'Occasional light humor' if params['humor'] > 0.3 else 'Minimal humor'}
- Emotional: {params['emotion']:.1f} - {'Deep emotional resonance' if params['emotion'] > 0.7 else 'Balanced emotion' if params['emotion'] > 0.3 else 'Factual and neutral'}
- Poetic: {params['poetic']:.1f} - {'Highly poetic and artistic' if params['poetic'] > 0.7 else 'Moderately poetic' if params['poetic'] > 0.3 else 'Simple and direct'}
- Metaphorical: {params['metaphorical']:.1f} - {'Rich in metaphors and analogies' if params['metaphorical'] > 0.7 else 'Some metaphorical elements' if params['metaphorical'] > 0.3 else 'Literal descriptions'}
- Technical: {params['technical']:.1f} - {'Include technical details' if params['technical'] > 0.7 else 'Balance of technical and simple' if params['technical'] > 0.3 else 'Simple, accessible language'}
"""

def create_user_prompt(count, mode):
    """Create a user prompt based on the generation mode and count"""
    unit = mode.rstrip('s')  # Remove potential plural
    return f"Generate {count} distinct {mode} about butter. Each {unit} should:\n" + \
           "- Be complete and grammatically correct\n" + \
           "- Focus on different aspects of butter (taste, cooking, history, etc.)\n" + \
           "- Vary in length and structure\n" + \
           "- Be suitable for use as placeholder text"
