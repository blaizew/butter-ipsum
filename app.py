import logging
import time
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

@app.route('/sheets')
def sheets_docs():
    return render_template('google_sheets.html')

@app.route('/generate', methods=['GET'])
def generate_text():
    """Generate butter-themed text through web interface."""
    try:
        # Parse and validate basic parameters
        count = int(request.args.get('count', 1))
        mode = request.args.get('mode', 'paragraph')
        use_gpt = request.args.get('use_gpt', '').lower() == 'true'
        
        # Get tuning parameters
        tuning_params = {
            'playfulness': int(request.args.get('playfulness', 7)),
            'humor': int(request.args.get('humor', 4)),
            'emotion': int(request.args.get('emotion', 6)),
            'poetic': int(request.args.get('poetic', 8)),
            'metaphorical': int(request.args.get('metaphorical', 8)),
            'technical': int(request.args.get('technical', 3))
        }
        
        # Validate parameters
        if count < 1 or count > 10:
            return jsonify({'error': 'Count must be between 1 and 10'}), 400
            
        if mode not in ['paragraph', 'sentence', 'word']:
            return jsonify({'error': 'Invalid mode'}), 400
            
        for param, value in tuning_params.items():
            if not isinstance(value, int) or value < 1 or value > 10:
                return jsonify({'error': f'Invalid {param} value. Must be between 1 and 10'}), 400

        # Create a new generator instance with current settings
        generator = ButterTextGenerator(use_gpt=use_gpt, tuning_params=tuning_params)
        
        # Check if GPT was requested but not available
        if use_gpt and not generator.use_gpt:
            if hasattr(generator.__class__, '_rate_limited_until'):
                remaining_time = int(generator.__class__._rate_limited_until - time.time())
                if remaining_time > 0:
                    logger.warning(f"GPT generation rate limited for {remaining_time} seconds")
                    return jsonify({
                        'text': None,
                        'error': f'GPT generation is temporarily unavailable due to rate limiting. Please try again in {remaining_time} seconds or disable GPT.',
                        'fallback_available': True
                    }), 503
            
            logger.warning("GPT generation requested but not available")
            return jsonify({
                'text': None,
                'error': 'GPT generation is currently unavailable. Please try again later or disable GPT.',
                'fallback_available': True
            }), 503
        
        # Generate text based on mode
        if mode == 'paragraph':
            logger.debug(f"Generating {count} paragraphs (GPT: {use_gpt})")
            text = generator.generate_paragraphs(count)
        elif mode == 'sentence':
            logger.debug(f"Generating {count} sentences (GPT: {use_gpt})")
            text = generator.generate_sentences(count)
        else:
            logger.debug(f"Generating {count} words (GPT: {use_gpt})")
            text = generator.generate_words(count)

        if text is None:
            return jsonify({
                'error': 'Failed to generate text',
                'fallback_available': True
            }), 500

        return jsonify({'text': text})
        
    except ValueError as ve:
        logger.error(f"Invalid parameter value: {str(ve)}")
        return jsonify({'error': 'Invalid parameter value'}), 400
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
