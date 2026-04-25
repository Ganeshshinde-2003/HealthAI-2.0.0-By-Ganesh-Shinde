"""
File Processing Utilities for HealthAI Backend
Handles extraction of text content from various file types.
"""

import os
import io
import fitz  # PyMuPDF
import pandas as pd
from docx import Document
from werkzeug.datastructures import FileStorage


class FileProcessingError(Exception):
    """Custom exception for file processing errors."""
    pass


def extract_text_from_file(uploaded_file):
    """
    Extracts text content from various file types (PDF, DOCX, XLSX, XLS, TXT, CSV).

    Args:
        uploaded_file: FileStorage object or file path

    Returns:
        str: Extracted text content

    Raises:
        FileProcessingError: If file processing fails

    Supported Formats:
        - PDF (.pdf)
        - Word (.docx)
        - Excel (.xlsx, .xls)
        - Plain Text (.txt)
        - CSV (.csv)
    """
    if uploaded_file is None:
        return ""

    # Handle FileStorage object
    if isinstance(uploaded_file, FileStorage):
        filename = uploaded_file.filename
        file_bytes = uploaded_file.read()
        uploaded_file.seek(0)  # Reset file pointer
    else:
        # Handle file path
        filename = os.path.basename(str(uploaded_file))
        with open(uploaded_file, 'rb') as f:
            file_bytes = f.read()

    file_extension = os.path.splitext(filename)[1].lower()

    # Supported extensions
    SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    # Validate file extension
    if file_extension not in SUPPORTED_EXTENSIONS:
        raise FileProcessingError(f"Unsupported file type: {file_extension}")

    # Validate file size
    if len(file_bytes) > MAX_FILE_SIZE:
        raise FileProcessingError(f"File exceeds maximum size of 10 MB")

    try:
        if file_extension == ".pdf":
            text = _extract_from_pdf(file_bytes, filename)

        elif file_extension == ".docx":
            text = _extract_from_docx(file_bytes, filename)

        elif file_extension in [".xlsx", ".xls"]:
            text = _extract_from_excel(file_bytes, filename)

        elif file_extension in [".txt", ".csv"]:
            text = file_bytes.decode('utf-8', errors='ignore')

        else:
            raise FileProcessingError(f"Unsupported file type: {file_extension}")

    except FileProcessingError:
        raise
    except Exception as e:
        raise FileProcessingError(f"Error processing file '{filename}': {str(e)}")

    # Warn if no text was extracted
    if not text.strip() and file_extension not in [".txt", ".csv"]:
        print(f"Warning: No readable text extracted from '{filename}'")

    return text


def _extract_from_pdf(file_bytes, filename):
    """Extract text from PDF file."""
    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text") + "\n"
        pdf_document.close()
        return text
    except Exception as e:
        raise FileProcessingError(f"Error processing PDF file '{filename}': {str(e)}")


def _extract_from_docx(file_bytes, filename):
    """Extract text from DOCX file."""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        raise FileProcessingError(f"Error processing DOCX file '{filename}': {str(e)}")


def _extract_from_excel(file_bytes, filename):
    """Extract text from Excel file."""
    try:
        excel_data = pd.read_excel(io.BytesIO(file_bytes), sheet_name=None)
        text = ""
        for sheet_name, df in excel_data.items():
            text += f"--- Sheet: {sheet_name} ---\n"
            text += df.to_string(index=False) + "\n\n"
        return text
    except Exception as e:
        raise FileProcessingError(f"Error processing Excel file '{filename}': {str(e)}")


def allowed_file(filename, allowed_extensions=None):
    """
    Check if file extension is allowed.

    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions (default: {'.pdf', '.docx', '.xlsx', '.xls', '.txt', '.csv'})

    Returns:
        bool: True if file extension is allowed
    """
    if allowed_extensions is None:
        allowed_extensions = {'.pdf', '.docx', '.xlsx', '.xls', '.txt', '.csv'}

    return '.' in filename and \
           os.path.splitext(filename)[1].lower() in allowed_extensions
