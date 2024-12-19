# Butter Ipsum 🧈

A deliciously smooth Lorem Ipsum generator that creates culinary-themed placeholder text. Perfect for food blogs, restaurant websites, and culinary applications.

## Features

- 🔄 **Dynamic Text Generation**: Create paragraphs, sentences, or individual words of butter-themed placeholder text
- 🌐 **RESTful API**: Integrate Butter Ipsum into your applications with our simple API
- 📊 **Google Sheets Integration**: Use custom functions to generate text directly in your spreadsheets
- ✨ **Contextual Generation**: Text generation that maintains food and culinary themes
- 🎯 **Multiple Output Formats**: Generate single words, sentences, or complete paragraphs
- 🔌 **Easy Integration**: Simple REST API with clear documentation

## Live Demo

Visit [Butter Ipsum Generator](https://butteripsum.com) to try it out!

## Installation

1. Clone the repository:
```bash
git clone https://github.com/blaizew/butter-ipsum.git
cd butter-ipsum
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`.

## Usage

### Web Interface

Visit the homepage and use the simple form interface to generate text:
1. Select your desired output format (paragraphs, sentences, or words)
2. Choose the number of units to generate
3. Click "Generate" to create your butter-themed text
4. Copy the generated text with a single click

### API Integration

Make GET requests to the API endpoint:

```bash
curl "https://butteripsum.com/api/v1/generate?count=2&mode=paragraph"
```

See our [API Documentation](https://butteripsum.com/api/docs) for detailed usage instructions.

### Google Sheets Integration

1. Open your Google Sheet
2. Go to Extensions > Apps Script
3. Copy the provided script from our [Google Sheets Integration Guide](https://butteripsum.com/sheets)
4. Use the `BUTTERIPSUM()` function in your spreadsheet:
```
=BUTTERIPSUM(2, "paragraph")  // Generates 2 paragraphs
=BUTTERIPSUM(3, "sentence")   // Generates 3 sentences
=BUTTERIPSUM(5, "word")       // Generates 5 words
```

## Development

Built with:
- Flask web framework
- Python backend with spaCy NLP
- Bootstrap for responsive design
- Google Apps Script integration

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the classic Lorem Ipsum and our love for butter
- Special thanks to all contributors and butter enthusiasts
