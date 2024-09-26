import ollama
from datetime import datetime
import time

valid_types = [ 'facture', 'devis', 'mail', 'arrêt maladie', 'impots', 'relevé de comptes', 'autres']

def retry_extraction(extraction_func, content, max_retries=3):
    """
    Generic retry function for extractions.
    
    :param extraction_func: The extraction function to retry.
    :param content: The document content to extract from.
    :param max_retries: Maximum number of retry attempts (default is 3).
    :return: Extracted information or None if all attempts fail.
    """
    for attempt in range(max_retries):
        try:
            result = extraction_func(content)
            return result
        except Exception as e:
            print(f"Error in {extraction_func.__name__} (Attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying ...")
    
    print(f"All retry attempts failed for {extraction_func.__name__}.")
    return None

def extract_date(content):
    """Extracts the date from the document content."""
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'user', 
            'content': f'Extract the date of document production in ISO format from this document. If unsure, provide your best guess. REPLY only a date with a function call ! THE RESULT MUST BE A DATE with FORMAT YYYY-MM-DD\n\n### Document Content ###\n{content}'
        }],
        tools=[{
            'type': 'function',
            'function': {
                'name': 'push_extracted_date',
                'description': 'Push extracted date',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'date': {   
                            'type': 'string',
                            'description': 'The date of the document in YYYY-MM-DD format.',
                        },
                    },
                    'required': ['date'],
                },
            },
        }],
    )
    
    print("Date extraction response:", response['message'])
    return response['message']['tool_calls'][0]['function']['arguments']

def extract_type(content):
    """Extracts the document type from the content."""
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'user', 
            'content': f'Determine the type of this document. Choose from: '+', '.join(valid_types)+'. \n\n### Document Content ###\n{content}'
        }],
        tools=[{
            'type': 'function',
            'function': {
                'name': 'push_extracted_type',
                'description': 'Push extracted document type',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'type': {
                            'type': 'string',
                            'description': 'The type of document.',
                            'enum': valid_types
                        },
                    },
                    'required': ['type'],
                },
            },
        }],
    )
    
    print("Type extraction response:", response['message'])
    return response['message']['tool_calls'][0]['function']['arguments']

def extract_emitter(content):
    """Extracts the emitter from the document content."""
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'user', 
            'content': f'Extract the name of the person or organization who sent or created this document. If unsure, provide your best guess.\n\n### Document Content ###\n{content}'
        }],
        tools=[{
            'type': 'function',
            'function': {
                'name': 'push_extracted_emitter',
                'description': 'Push extracted emitter',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'emitter': {
                            'type': 'string',
                            'description': 'The name of the person or organization who sent or created the document. Must be a simple name without special characters. Can\'t be a long phrase.',
                        },
                    },
                    'required': ['emitter'],
                },
            },
        }],
    )
    
    print("Emitter extraction response:", response['message'])
    return response['message']['tool_calls'][0]['function']['arguments']

def extract_recipient(content):
    """Extracts the recipient from the document content."""
    response = ollama.chat(
        model='llama3.2',
        messages=[{
            'role': 'user', 
            'content': f'Extract the name of the person or organization who received this document. If unsure, provide your best guess.\n\n### Document Content ###\n{content}'
        }],
        tools=[{
            'type': 'function',
            'function': {
                'name': 'push_extracted_recipient',
                'description': 'Push extracted recipient',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'recipient': {
                            'type': 'string',
                            'description': 'The name of the person or organization who received the document.',
                             'enum': ['Jérôme', 'Pauline', 'Grégoire', 'OLTMANNS', 'WAX']
                        },
                    },
                    'required': ['recipient'],
                },
            },
        }],
    )
    
    print("Recipient extraction response:", response['message'])
    return response['message']['tool_calls'][0]['function']['arguments']

def analyze_document(content, max_retries=3):
    """
    Analyzes the document content to extract required information using the Llama model.
    
    :param content: The text content of the document.
    :param max_retries: Maximum number of retry attempts for each extraction (default is 3).
    :return: A dictionary containing extracted information or None if critical extractions fail.
    """
    extracted_info = {}

    # Extract date with retry
    date_info = retry_extraction(extract_date, content, max_retries)
    if date_info:
        extracted_info.update(date_info)
    else:
        print("Failed to extract date after all retries. Aborting analysis.")
        return None

    # Extract type with retry
    type_info = retry_extraction(extract_type, content, max_retries)
    if type_info:
        extracted_info.update(type_info)
    else:
        print("Failed to extract document type after all retries. Aborting analysis.")
        return None

    # Extract emitter with retry
    emitter_info = retry_extraction(extract_emitter, content, max_retries)
    if emitter_info:
        extracted_info.update(emitter_info)
    else:
        print("Failed to extract emitter after all retries. Continuing with partial information.")

    # Extract recipient with retry
    recipient_info = retry_extraction(extract_recipient, content, max_retries)
    if recipient_info:
        extracted_info.update(recipient_info)
    else:
        print("Failed to extract recipient after all retries. Continuing with partial information.")

    try:
        # Validate date format
        datetime.strptime(extracted_info['date'], "%Y-%m-%d")
        
        # Validate document type
        if extracted_info['type'] not in valid_types:
            raise ValueError(f"Invalid document type: {extracted_info['type']}")
        
        print("Final extracted information:", extracted_info)
        return extracted_info

    except Exception as e:
        print(f"Error in final validation: {str(e)}")
        return None