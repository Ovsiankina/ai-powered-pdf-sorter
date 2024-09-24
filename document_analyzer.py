import re
from datetime import datetime
import ollama

def analyze_document(content):
    """
    Analyzes the document content to extract required information.
    
    :param content: The text content of the document.
    :return: A dictionary containing extracted information.
    """
    # Use ollama to extract information
    response = ollama.generate(
        model='llama3.1',
        prompt=f"""Analyze the following document content and extract these information:
        1. Document date (format as YYYY-MM-DD)
        2. Document type (relevé de comptes, facture, devis, mail, arrêt maladie)
        3. Emitter of the document
        4. Recipient of the document

        Document content:
        {content}

        Respond in JSON format:
        {{
            "date": "YYYY-MM-DD",
            "type": "document_type",
            "emitter": "emitter_name",
            "recipient": "recipient_name"
        }}
        """
    )

    try:
        info = eval(response['response'])  # Convert string to dictionary
        return info
    except:
        print("Error parsing ollama response")
        return None