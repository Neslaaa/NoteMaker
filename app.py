

from flask import Flask, render_template, request
import fitz
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        return "No file selected"

    file = request.files['file']

    if file.filename == '':
        return "Please select a file"

    if not file.filename.lower().endswith('.pdf'):
        return "Please upload a PDF file"

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    document = fitz.open(filepath)

    extracted_text = ""

    for page in document:
        extracted_text += page.get_text()

    document.close()

    return render_template(
        'index.html',
        extracted_text=extracted_text
    )


if __name__ == '__main__':
    app.run(debug=True)

