from flask import Flask, request, render_template_string, redirect, url_for, flash
import google.generativeai as genai
import os
import tempfile
from PIL import Image
import fitz  # PyMuPDF for PDF processing
import io
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure Google GenAI
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is required. Please set it in Railway dashboard.")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text_from_image(image_data):
    """Extract text from image using Google GenAI"""
    try:
        # Convert image data to PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to base64 for Gemini API
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Create the prompt for OCR
        prompt = "Extract all text from this image. Return only the extracted text, no additional formatting or explanations."
        
        # Use Gemini to extract text
        response = model.generate_content([prompt, {"mime_type": "image/png", "data": img_base64}])
        
        if not response.text:
            return "No text could be extracted from the image."
        
        return response.text
    except Exception as e:
        return f"Error processing image: {str(e)}"

def extract_text_from_pdf(pdf_data):
    """Extract text from PDF using PyMuPDF and then process images with GenAI"""
    try:
        # Open PDF with PyMuPDF
        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        extracted_text = ""
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            
            # First try to extract text directly from PDF
            page_text = page.get_text()
            if page_text.strip():
                extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            else:
                # If no text found, convert page to image and use OCR
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                ocr_text = extract_text_from_image(img_data)
                extracted_text += f"\n--- Page {page_num + 1} (OCR) ---\n{ocr_text}\n"
        
        pdf_document.close()
        return extracted_text
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

@app.route('/')
def index():
    """Main page with file upload form"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OCR Web Application</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .upload-area {
            border: 2px dashed #007bff;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            border-color: #0056b3;
            background-color: #e3f2fd;
        }
        .file-input {
            margin: 20px 0;
        }
        input[type="file"] {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: 100%;
            max-width: 400px;
        }
        .submit-btn {
            background-color: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .submit-btn:hover {
            background-color: #0056b3;
        }
        .result-area {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        .error {
            color: #dc3545;
            background-color: #f8d7da;
            border-color: #f5c6cb;
        }
        .success {
            color: #155724;
            background-color: #d4edda;
            border-color: #c3e6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>OCR Web Application</h1>
        <p>Upload an image or PDF file to extract text using Google Gemini AI</p>
        
        <form action="/upload" method="post" enctype="multipart/form-data">
            <div class="upload-area">
                <h3>Choose File</h3>
                <p>Supported formats: JPG, PNG, PDF</p>
                <div class="file-input">
                    <input type="file" name="file" accept=".jpg,.jpeg,.png,.pdf" required>
                </div>
                <br>
                <button type="submit" class="submit-btn">Extract Text</button>
            </div>
        </form>
    </div>
</body>
</html>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and OCR processing"""
    try:
        if 'file' not in request.files:
            flash('No file uploaded. Please select a file and try again.')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected. Please select a file and try again.')
            return redirect(url_for('index'))
        
        # Read file content
        file_content = file.read()
        file_extension = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        # Process based on file type
        if file_extension in ['jpg', 'jpeg', 'png']:
            extracted_text = extract_text_from_image(file_content)
        elif file_extension == 'pdf':
            extracted_text = extract_text_from_pdf(file_content)
        else:
            flash(f'Unsupported file format: {file_extension}. Please upload JPG, PNG, or PDF files.')
            return redirect(url_for('index'))
        
        # Display results
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OCR Results</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .result-area {
            margin-top: 30px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        .success {
            color: #155724;
            background-color: #d4edda;
            border-color: #c3e6cb;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>OCR Results</h1>
        <div class="result-area success">
            <h3>Extracted Text from {{ filename }}:</h3>
            <pre>{{ extracted_text }}</pre>
        </div>
        <br>
        <a href="/">← Upload Another File</a>
    </div>
</body>
</html>
        ''', filename=file.filename, extracted_text=extracted_text)
        
    except Exception as e:
        flash(f'An error occurred while processing the file: {str(e)}')
        return redirect(url_for('index'))

if __name__ == "__main__":
    # Validate API key on startup
    try:
        # Test the API key by making a simple request
        test_response = model.generate_content("Hello")
        print("✅ Google GenAI API key is valid")
    except Exception as e:
        print(f"❌ Google GenAI API key validation failed: {str(e)}")
        print("Please set a valid GEMINI_API_KEY environment variable in Railway dashboard")
    
    # Use Railway's PORT environment variable or default to 3000
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, debug=False)