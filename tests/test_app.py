"""Basic tests for the NoteMaker Flask application."""
import io
import os
import unittest

import fitz

import app as notemaker


class NoteMakerTests(unittest.TestCase):
    def setUp(self):
        notemaker.app.config["TESTING"] = True
        self.client = notemaker.app.test_client()

    def tearDown(self):
        # Remove any file created by the successful-upload test.
        uploaded_path = os.path.join("uploads", "test_notes.pdf")
        if os.path.exists(uploaded_path):
            os.remove(uploaded_path)

    def make_pdf(self):
        document = fitz.open()
        page = document.new_page()
        page.insert_text((72, 72), "NoteMaker test content")
        data = document.tobytes()
        document.close()
        return data

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to NoteMaker", response.data)

    def test_missing_file_field(self):
        response = self.client.post("/upload", data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No file selected", response.data)

    def test_rejects_non_pdf_filename(self):
        response = self.client.post(
            "/upload",
            data={"file": (io.BytesIO(b"not a pdf"), "notes.txt")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Please upload a PDF file", response.data)

    def test_uploads_pdf_and_extracts_text(self):
        response = self.client.post(
            "/upload",
            data={"file": (io.BytesIO(self.make_pdf()), "test_notes.pdf")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NoteMaker test content", response.data)


if __name__ == "__main__":
    unittest.main()
