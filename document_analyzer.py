import ollama
from datetime import datetime

def analyze_document(content):
    """
    Analyzes the document content to extract required information using the Llama model.
    
    :param content: The text content of the document.
    :return: A dictionary containing extracted information.
    """
    response = ollama.chat(
        model='llama3.1',
        messages=[{
            'role': 'user', 
            'content': f'Extract the following information from this document: date, type, emitter, and recipient. Think step by step to achieve the goal.\n\n### Document Content ###\n{content}'
        }],
        tools=[{
            'type': 'function',
            'function': {
                'name': 'extract_document_info',
                'description': 'Extract and structure document information',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'date': {
                            'type': 'string',
                            'description': 'The date of the document in YYYY-MM-DD format. Example: 2024-08-01',
                        },
                        'type': {
                            'type': 'string',
                            'description': 'The type of document. Must be one of: relevé de comptes, facture, devis, mail, arrêt maladie',
                            'enum': ['relevé de comptes', 'facture', 'devis', 'mail', 'arrêt maladie']
                        },
                        'emitter': {
                            'type': 'string',
                            'description': 'The name of the person or organization who sent or created the document. Example: Société XYZ',
                        },
                        'recipient': {
                            'type': 'string',
                            'description': 'The name of the person or organization who received the document. Example: Jean Dupont',
                        }
                    },
                    'required': ['date', 'type', 'emitter', 'recipient'],
                },
            },
        }],
    )

    try:
        if not response['message'].get('tool_calls'):
            print("The model didn't use the function. Its response was:")
            print(response['message']['content'])
            return None

        for tool in response['message']['tool_calls']:
            if tool['function']['name'] == 'extract_document_info':
                info = eval(tool['function']['arguments'])
                
                # Validate date format
                datetime.strptime(info['date'], "%Y-%m-%d")
                
                # Validate document type
                valid_types = ['relevé de comptes', 'facture', 'devis', 'mail', 'arrêt maladie']
                if info['type'] not in valid_types:
                    raise ValueError(f"Invalid document type: {info['type']}")
                
                return info
        
        print("No valid information extracted")
        return None
    except Exception as e:
        print(f"Error parsing Llama response: {str(e)}")
        return None