# NoteMaker

NoteMaker is a small Python web application that lets a user upload a PDF study document and view the text extracted from it in a browser.

> **Current implementation note:** The submitted version extracts and displays PDF text. It does not currently perform automatic summarisation, key-point ranking, or machine-learning predictions. The page's introductory wording can be updated if needed so that it describes the implemented feature accurately.

## 1. Problem statement

Students often have study material stored in PDF files. Reading or copying text from a PDF can be inconvenient when they want to view its text in one place. NoteMaker provides a simple browser-based way to upload a PDF and display its extractable text.

## 2. Objective

- Provide a simple web page for PDF uploads.
- Check that a file has been selected and that its filename has a PDF extension.
- Extract text from the uploaded PDF using PyMuPDF.
- Display the extracted text on the result page.

## 3. Proposed solution

The user opens the Flask website, selects a PDF and submits the upload form. Flask receives the file, checks the request and filename, saves the file in the `uploads` directory, and uses PyMuPDF to read text from each page. The extracted text is passed to the HTML template and displayed in the browser.

## 4. Project architecture

```text
notesmaker/
├── app.py                 # Flask routes and PDF extraction logic
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Files excluded from version control
├── templates/
│   └── index.html         # Upload form and extracted-text display
├── static/
│   └── style.css          # Website styling
├── uploads/
│   └── .gitkeep           # Keeps the upload directory in the project
└── tests/
    └── test_app.py        # Basic automated tests
```

### Request flow

1. The browser requests `/` and Flask returns `templates/index.html`.
2. The user selects a PDF and submits the form to `/upload` using POST.
3. Flask checks the uploaded file and saves it in `uploads/`.
4. PyMuPDF opens the PDF and extracts text page by page.
5. Flask sends the extracted text to the HTML template, which displays it.

## 5. Data source and processing workflow

- **Data source:** A PDF file selected and supplied by the user. The project does not use an external dataset.
- **Loading:** Flask receives the uploaded file through the multipart form request.
- **Validation:** The route checks whether the `file` field exists, whether a filename was supplied, and whether the filename ends in `.pdf` (case-insensitive).
- **Storage:** The filename is passed through Werkzeug's `secure_filename` before saving in `uploads/`.
- **Extraction:** PyMuPDF (`fitz`) opens the saved PDF. The application loops through each page and appends the text returned by `page.get_text()`.
- **Transformation:** Page text is combined into one string and passed to the HTML template. Newline characters are displayed as line breaks.
- **Cleaning and feature preparation:** No advanced text cleaning, tokenisation, feature engineering, or model input preparation is performed in this version.
- **Data quality limitations:** Scanned PDFs that contain only images may not provide extractable text. Complex layouts, tables, columns, and unusual fonts may not be extracted in their original visual order.

## 6. Technologies used

- **Python:** Main programming language.
- **Flask:** Handles web routes, requests, and HTML rendering.
- **PyMuPDF:** Reads PDF pages and extracts text.
- **Werkzeug:** Provides `secure_filename` for safer uploaded filenames.
- **HTML:** Defines the upload form and result display.
- **CSS:** Styles the web page.

## 7. Setup instructions

Python 3 should be installed.

1. Open a terminal in the project directory.
2. (Recommended) Create and activate a virtual environment:

   ```bash
   py -m venv .venv
   .venv\\Scripts\\activate
   ```

3. Install the dependencies:

   ```bash
   py -m pip install -r requirements.txt
   ```

## 8. How to run the project

From the project directory, run:

```bash
py app.py
```

Open `http://127.0.0.1:5000` in a browser. Select a PDF and click **Upload PDF**. The extracted text appears below the form.

For local development, Flask's debug mode is enabled in the current application. Do not use the development server or debug mode as a public production deployment.

## 9. How to run tests

Install the dependencies, then run this command from the project directory:

```bash
py -m unittest discover -s tests -v
```

The tests use Flask's test client and create a small PDF in memory for the upload test. They check the home page, missing-file handling, rejection of a non-PDF filename, and successful PDF text extraction.

## 10. Results and outputs

The implemented output is the text extracted from the uploaded PDF and displayed on the website. The application does not currently calculate model metrics, predictions, accuracy, or visual analytics because no machine-learning model or statistical analysis is implemented.

## 11. Engineering decisions

- Flask was selected to keep the web application small and straightforward.
- The upload form uses POST and `multipart/form-data` because it sends a file to the server.
- PyMuPDF was selected to read PDF page text from Python.
- `secure_filename` is used to reduce risks from unsafe filenames.
- The HTML template and CSS are kept separate from Python logic to make the interface easier to maintain.
- Basic automated tests use Flask's test client so routes can be checked without manually opening a browser.

### Error handling and current limitations

The upload route returns a message if the file field is missing, no file is selected, or the filename does not end in `.pdf`. The current implementation does not yet provide a custom error page for corrupted or password-protected PDFs, enforce a maximum upload size, or restrict uploads to a private temporary directory. It also does not include application logging or a database.

## 12. Research notes

| Topic researched | What was learned and how it was applied |
|---|---|
| Flask routes | A route connects a URL and HTTP method to a Python function. The `/` and `/upload` routes handle the home page and PDF submission. |
| HTML file upload | A form needs `method="POST"` and `enctype="multipart/form-data"` to send a file. The upload form uses these settings. |
| PyMuPDF | PyMuPDF opens PDF documents and provides page-level text extraction. The application loops through pages and calls `get_text()`. |
| Filename handling | `secure_filename` creates a safer filename before the uploaded file is saved. |
| Flask templates | `render_template` sends data from Python to an HTML template. The extracted text is passed to `index.html`. |

## 13. Future improvements

- Add genuine automatic summarisation or important-point extraction and evaluate its quality.
- Add support for scanned PDFs using OCR.
- Add file-size limits and stronger file-content validation.
- Handle corrupted and password-protected PDFs with user-friendly messages.
- Add a download option for processed notes.
- Add more automated tests and application logging.

## 14. Reproducibility

The dependency list is recorded in `requirements.txt`. Install it using the setup instructions and run the application from the project directory. The tests can be rerun using the command in the testing section. User-uploaded PDFs are runtime files and are excluded from version control by `.gitignore`.
