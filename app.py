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

@app.route('/generate', methods=['GET'])
def generate_text():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
