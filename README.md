# OCR Web Application

A web application built with FastHTML and Google GenAI for Optical Character Recognition (OCR) from uploaded images and PDF files.

## Features

- Upload and process images (JPG, PNG) and PDF files
- Extract text using Google Gemini AI
- Modern, responsive web interface
- Docker containerization support
- Error handling and file validation

## Prerequisites

- Python 3.11+
- Docker (optional)
- Google GenAI API key

## Installation

### Local Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the API key in `app.py`:
   ```python
   genai.configure(api_key="YOUR_ACTUAL_API_KEY")
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:3000`

### Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t ocr-app .
   ```

2. Run the container:
   ```bash
   docker run -p 3000:3000 ocr-app
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Usage

1. Open the web application in your browser
2. Click "Choose File" and select an image or PDF file
3. Click "Extract Text" to process the file
4. View the extracted text in the results area

## Supported File Formats

- Images: JPG, JPEG, PNG
- Documents: PDF

## API Endpoints

- `GET /` - Main upload page
- `POST /upload` - File upload and OCR processing

## Dependencies

- FastHTML: Web framework
- Google Generative AI: OCR processing
- Pillow: Image processing
- PyMuPDF: PDF processing
- python-multipart: File upload handling

## Configuration

The application runs on port 3000 by default. To change this, modify the `run(port=3000)` line in `app.py`.

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Processing errors
- API failures
- File upload issues
