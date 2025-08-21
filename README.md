# Image Studio

A web-based image processing application that allows users to manipulate and enhance images using various tools and effects.

## Features

- Image upload and processing
- Background removal
- Image enhancement
- Profile picture optimization
- Secure file handling
- Real-time preview
- Support for multiple image formats

## Tech Stack

- Backend: Python (Flask)
- Frontend: HTML, CSS, JavaScript
- Image Processing: Custom Python libraries
- API Integration: Groq API for enhanced processing

## Setup

1. Clone the repository:
```bash
git clone https://github.com/SubrataD27/Image-Studio.git
cd Image-Studio
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Environment Setup:
   - Create a `.env` file in the root directory
   - Add your API keys and configuration (see `.env.example` for reference)

4. Run the application:
```bash
python app.py
```

## Project Structure

```plaintext
├── app.py              # Main Flask application
├── check.py            # Image processing logic
├── requirements.txt    # Python dependencies
├── static/            
│   ├── css/           # Stylesheets
│   ├── images/        # Static images
│   ├── js/            # JavaScript files
│   ├── results/       # Processed images
│   └── uploads/       # Temporary upload storage
└── templates/         # HTML templates
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Code citations and references are available in `templates/# Code Citations.md`
- Thanks to all contributors and users of Image Studio
