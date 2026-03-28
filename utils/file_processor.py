"""
File Processing Utilities for HealthAI

Handles extraction of text content from various file types.
"""

import os
import io
import fitz  # PyMuPDF
import pandas as pd
from docx import Document
import streamlit as st
from config import FileConfig


@st.cache_data(show_spinner=False)
def extract_text_from_file(uploaded_file):
    """
    Extracts text content from various file types (PDF, DOCX, XLSX, XLS, TXT, CSV).

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text content or error marker

    Supported Formats:
        - PDF (.pdf)
        - Word (.docx)
        - Excel (.xlsx, .xls)
        - Plain Text (.txt)
        - CSV (.csv)
    """
    if uploaded_file is None:
        return ""

    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    text = ""

    # Validate file extension
    if file_extension not in FileConfig.SUPPORTED_EXTENSIONS:
        st.warning(f"Unsupported file type: {file_extension} for file '{uploaded_file.name}'")
        return "[Unsupported File Type Uploaded]"

    # Validate file size
    file_bytes = uploaded_file.getvalue()
    if len(file_bytes) > FileConfig.MAX_FILE_SIZE:
        st.error(f"File '{uploaded_file.name}' exceeds maximum size of {FileConfig.MAX_FILE_SIZE / (1024*1024):.1f} MB")
        return "[File Too Large]"

    try:
        if file_extension == ".pdf":
            text = _extract_from_pdf(file_bytes, uploaded_file.name)

        elif file_extension == ".docx":
            text = _extract_from_docx(file_bytes, uploaded_file.name)

        elif file_extension in [".xlsx", ".xls"]:
            text = _extract_from_excel(file_bytes, uploaded_file.name)

        elif file_extension in [".txt", ".csv"]:
            text = file_bytes.decode(FileConfig.TEXT_ENCODING, errors=FileConfig.ENCODING_ERROR_HANDLING)

    except Exception as e:
        st.error(f"An error occurred while processing '{uploaded_file.name}': {e}")
        return "[Error Processing File]"

    # Warn if no text was extracted
    if not text.strip() and file_extension not in [".txt", ".csv"]:
        st.warning(
            f"No readable text extracted from '{uploaded_file.name}'. "
            f"The file might be scanned, empty, or have complex formatting. "
            f"Consider pasting the text manually."
        )

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
        st.error(f"Error processing PDF file '{filename}': {e}")
        return "[Error Processing PDF File]"


def _extract_from_docx(file_bytes, filename):
    """Extract text from DOCX file."""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error processing DOCX file '{filename}': {e}")
        return "[Error Processing DOCX File]"


def _extract_from_excel(file_bytes, filename):
    """Extract text from Excel file."""
    try:
        excel_data = pd.read_excel(io.BytesIO(file_bytes), sheet_name=None)
        text = ""
        for sheet_name, df in excel_data.items():
            text += f"--- Sheet: {sheet_name} ---\n"
            text += df.to_string(index=False) + "\n\n"
        return text
    except Exception as excel_e:
        st.warning(
            f"Could not read Excel file '{filename}'. "
            f"Ensure 'openpyxl' (for .xlsx) or 'xlrd' (for .xls) is installed. "
            f"Error: {excel_e}"
        )
        return f"[Could not automatically process Excel file {filename} - Please try pasting the text or saving as PDF/TXT.]"
