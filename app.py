import logging
from flask import Flask, render_template, jsonify, request
from text_generator import ButterTextGenerator

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
text_generator = ButterTextGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/docs')
def api_docs():
    return render_template('api.html')

@app.route('/generate', methods=['GET'])
def generate_text():
    """Generate butter-themed text through web interface."""
    try:
        count = int(request.args.get('count', 1))
        mode = request.args.get('mode', 'paragraph')
        
        if count < 1 or count > 10:
            return jsonify({'error': 'Count must be between 1 and 10'}), 400
            
        if mode not in ['paragraph', 'sentence', 'word']:
            return jsonify({'error': 'Invalid mode'}), 400

        if mode == 'paragraph':
            logger.debug(f"Generating {count} paragraphs")
            text = text_generator.generate_paragraphs(count)
        elif mode == 'sentence':
            logger.debug(f"Generating {count} sentences")
            text = text_generator.generate_sentences(count)
        else:
            logger.debug(f"Generating {count} words")
            text = text_generator.generate_words(count)

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
        
        if count < 1 or count > 10:
            return jsonify({
                'error': 'Invalid count parameter',
                'message': 'Count must be between 1 and 10'
            }), 400
            
        if mode not in ['paragraph', 'sentence', 'word']:
            return jsonify({
                'error': 'Invalid mode parameter',
                'message': 'Mode must be one of: paragraph, sentence, word'
            }), 400

        if mode == 'paragraph':
            logger.debug(f"API: Generating {count} paragraphs")
            text = text_generator.generate_paragraphs(count)
        elif mode == 'sentence':
            logger.debug(f"API: Generating {count} sentences")
            text = text_generator.generate_sentences(count)
        else:
            logger.debug(f"API: Generating {count} words")
            text = text_generator.generate_words(count)

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
