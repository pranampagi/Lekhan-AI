import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """Extract raw text content from a PDF file.

    Uses pdfplumber to read each page and concatenate the text.
    Returns the full extracted text as a single string.

    Args:
        file_path: Path to the PDF file on disk.

    Returns:
        Extracted text content from all pages.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If the PDF cannot be parsed.
    """
    text_pages = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_pages.append(page_text)

    return "\n\n".join(text_pages)


def extract_text_from_txt(file_path: str) -> str:
    """Read raw text content from a plain text file.

    Args:
        file_path: Path to the text file on disk.

    Returns:
        Full text content of the file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text(file_path: str) -> str:
    """Extract text from a file based on its extension.

    Supports PDF (.pdf) and plain text (.txt) files.

    Args:
        file_path: Path to the file on disk.

    Returns:
        Extracted text content.

    Raises:
        ValueError: If the file type is not supported.
    """
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
