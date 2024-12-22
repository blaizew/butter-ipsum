import logging
from flask import Flask, render_template, jsonify, request
from text_generator import ButterTextGenerator
from gpt_generator import GPTTextGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
butter_generator = ButterTextGenerator()
gpt_generator = GPTTextGenerator(api_key="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", instructions_file="gpt_instructions") #Added API Key and instructions file
use_gpt = False #Added a toggle for GPT

@app.route('/')
def index():
    global use_gpt #Access the global variable
    return render_template('index.html', use_gpt=use_gpt) #Pass the toggle state to the template

@app.route('/api/docs')
def api_docs():
    return render_template('api.html')
@app.route('/sheets')
def sheets_docs():
    return render_template('google_sheets.html')


@app.route('/generate', methods=['GET'])
def generate_text():
    """Generate butter-themed text through web interface."""
    try:
        count = int(request.args.get('count', 1))
        mode = request.args.get('mode', 'paragraph')
        
        use_gpt = request.args.get('use_gpt', 'false').lower() == 'true'
        
        if use_gpt:
            logger.debug(f"Using GPT to generate {count} {mode}(s)")
            text = gpt_generator.generate_text(count, mode)
        else:
            if mode == 'paragraph':
                logger.debug(f"Generating {count} paragraphs")
                text = butter_generator.generate_paragraphs(count)
            elif mode == 'sentence':
                logger.debug(f"Generating {count} sentences")
                text = butter_generator.generate_sentences(count)
            else:
                logger.debug(f"Generating {count} words")
                text = butter_generator.generate_words(count)

        return jsonify({'text': text})
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        return jsonify({'error': 'Failed to generate text'}), 500

@app.route('/api/v1/generate', methods=['GET'])
def api_generate_text():
    """
    Generate butter-themed placeholder text through API.
    
    Query Parameters:
    - count (int): Number of units to generate (1-10)
    - mode (str): Generation mode ('paragraph', 'sentence', or 'word')
    
    Returns:
    JSON object containing:
    - text (str): Generated butter-themed text
    - metadata (object):
        - count (int): Number of units generated
        - mode (str): Generation mode used
        - timestamp (str): Generation timestamp
    
    Example:
    GET /api/v1/generate?count=2&mode=paragraph
    
    Error Codes:
    - 400: Invalid parameters
    - 500: Server error
    """
    try:
        count = int(request.args.get('count', 1))
        mode = request.args.get('mode', 'paragraph')
        
        use_gpt = request.args.get('use_gpt', 'false').lower() == 'true'
        
        if use_gpt:
            logger.debug(f"API: Using GPT to generate {count} {mode}(s)")
            text = gpt_generator.generate_text(count, mode)
        else:
            if mode == 'paragraph':
                logger.debug(f"API: Generating {count} paragraphs")
                text = butter_generator.generate_paragraphs(count)
            elif mode == 'sentence':
                logger.debug(f"API: Generating {count} sentences")
                text = butter_generator.generate_sentences(count)
            else:
                logger.debug(f"API: Generating {count} words")
                text = butter_generator.generate_words(count)

        from datetime import datetime
        return jsonify({
            'text': text,
            'metadata': {
                'count': count,
                'mode': mode,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        })
    except ValueError:
        return jsonify({
            'error': 'Invalid parameter type',
            'message': 'Count must be a valid integer'
        }), 400
    except Exception as e:
        logger.error(f"API Error generating text: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'Failed to generate text'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)