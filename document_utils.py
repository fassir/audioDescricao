import os
from pypdf import PdfReader

def extract_text_from_file(filepath):
    """
    Extracts text from a file based on its extension.
    Supports .pdf and .txt
    """
    if not os.path.exists(filepath):
        return None
        
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        if ext == '.pdf':
            return _extract_from_pdf(filepath)
        elif ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"Error: Unsupported file format {ext}"
    except Exception as e:
        return f"Error reading file: {e}"

def _extract_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            # Try to preserve paragraph structure
            # If a line ends with a period, !, or ?, it's likely end of sentence.
            # But PDFs often break lines arbitrarily.
            # A simple approach: add double newline between pages, 
            # and maybe rely on existing double newlines if pypdf captures them.
            # Let's just ensure pages are separated by double newlines at least.
            text += page_text + "\n\n"
    
    # Optional: Basic cleanup
    # Replace single newlines that are likely mid-sentence line breaks? 
    # This is risky without advanced logic. Let's keep it simple for now but ensure \n\n exists.
    return text
