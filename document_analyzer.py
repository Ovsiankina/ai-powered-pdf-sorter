import ollama
from datetime import datetime
import time
import json
from colorama import Fore, Style

valid_types = {
    "facture": "A bill or invoice for goods or services",
    "devis": "A quote or estimate for goods or services",
    "mail": "An email or written correspondence",
    "arrêt maladie": "A medical certificate or sick leave document",
    "impots": "Tax-related documents or forms",
    "relevé de comptes": "Bank statement or account summary",
    "autres": "Any other type of document not fitting the above categories",
}

ollamaModel = "Llama3.2"


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
            print(
                f"{Fore.YELLOW}Error in {extraction_func.__name__} (Attempt {
                    attempt + 1}/{max_retries}): {str(e)}{Style.RESET_ALL}"
            )
            if attempt < max_retries - 1:
                print(f"{Fore.YELLOW}Retrying ...{Style.RESET_ALL}")

    print(
        f"{Fore.RED}All retry attempts failed for {
            extraction_func.__name__}.{Style.RESET_ALL}"
    )
    return None


def extract_subject(content):
    """Extracts the subject from the document content."""
    response = ollama.chat(
        model=ollamaModel,
        messages=[
            {
                "role": "system",
                "content": "You are an expert document analyzer specializing in date extraction. Your task is to accurately identify and extract the subject of the document from the given content.",
            },
            {
                "role": "user",
                "content": f"""Analyze the following document content and extract the date of document production.

Instructions:
1. Carefully read through the entire document.
2. Look for any titles or subjects of the document. Focus on what summerizes clearly the nature of the document.
3. If there's no clear titles or subjects, make one yourself that summerizes quickly in short terms what is the nature of this document.

Examples:
Input: "CERTIFICAT MÉDICAL"
Output: {{"subject": "CERTIFICAT MÉDICAL",
    "reasoning": "The subject of the document is clearly stating that this is a medical certificate."}}

Input (Without a clear title): "Facture n 2329 - Loyer mensuel fèvr - Studio "
Output: {{"subject": "Loyer Mensuel Studio",
    "reasoning": "The document doesn't have a clear title but it's clearly a bill for february's rent."}}

Now, analyze this document content:

{content}

Provide your extraction using the push_extracted_date function.""",
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "push_extracted_date",
                    "description": "Push extracted date and reasoning",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "subject": {
                                "type": "string",
                                "description": "The title or subject of the document.",
                            },
                            "reasoning": {
                                "type": "string",
                                "description": "Explanation for the chosen title or subject and where it has been found in the document or not.",
                            },
                        },
                        "required": ["subject", "reasoning"],
                    },
                },
            }
        ],
    )

    # return json.loads(response['message']['tool_calls'][0]['function']['arguments'])
    return response["message"]["tool_calls"][0]["function"]["arguments"]


def extract_date(content):
    """Extracts the date from the document content."""
    response = ollama.chat(
        model=ollamaModel,
        messages=[
            {
                "role": "system",
                "content": "You are an expert document analyzer specializing in date extraction. Your task is to accurately identify and extract the date of document production from the given content.",
            },
            {
                "role": "user",
                "content": f"""Analyze the following document content and extract the date of document production.

Instructions:
1. Carefully read through the entire document.
2. Look for any mentions of dates, focusing on those that seem to indicate when the document was created or issued.
3. If multiple dates are present, use context to determine which is most likely the document production date.
4. If no explicit date is found, use any contextual clues to make your best estimate.
5. Format the date as YYYY-MM-DD.
6. If the day is uncertain, use the first day of the month (01).
7. If the month is uncertain, use January (01).
8. Provide your reasoning for the chosen date.

Examples:
Input: "Invoice dated 15/04/2023 for services rendered in March 2023"
Output: {{"date": "2023-04-15",
    "reasoning": "Explicit invoice date provided in DD/MM/YYYY format."}}

Input: "Quarterly report - Q2 2023"
Output: {{"date": "2023-04-01",
    "reasoning": "Document is for Q2 2023. Used the first day of the quarter as the best estimate."}}

Now, analyze this document content:

{content}

Provide your extraction using the push_extracted_date function.""",
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "push_extracted_date",
                    "description": "Push extracted date and reasoning",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "date": {
                                "type": "string",
                                "description": "The date of the document in YYYY-MM-DD format.",
                            },
                            "reasoning": {
                                "type": "string",
                                "description": "Explanation for the chosen date.",
                            },
                        },
                        "required": ["date", "reasoning"],
                    },
                },
            }
        ],
    )

    # return json.loads(response['message']['tool_calls'][0]['function']['arguments'])
    return response["message"]["tool_calls"][0]["function"]["arguments"]


def extract_type(content):
    """Extracts the document type from the content."""
    type_descriptions = "\n".join(
        [f"- {type}: {description}" for type, description in valid_types.items()]
    )

    response = ollama.chat(
        model=ollamaModel,
        messages=[
            {
                "role": "system",
                "content": "You are an expert document classifier with deep knowledge of various document types and their characteristics.",
            },
            {
                "role": "user",
                "content": f"""Analyze the following document content and determine its type based on the given categories.

Document Types:
{type_descriptions}

Instructions:
1. Carefully read through the entire document content.
2. Consider the structure, language, and purpose of the document.
3. Match the document's characteristics to the most appropriate type from the list provided.
4. If uncertain between multiple types, explain your reasoning for each possibility.
5. If no type seems to fit well, use 'autres' and explain why.

Thought Process:
1. What is the main purpose of this document?
2. What key features or sections does it contain?
3. How does its structure compare to typical examples of each document type?
4. Are there any specific keywords or phrases that strongly indicate a particular type?

Examples:
Input: "Dear Mr. Smith, Thank you for your interest in our services. Please find attached our quote for the project discussed..."
Output: {{"type": "devis", "reasoning": "The document is clearly offering a quote for services, which matches the description of 'devis'."}}

Input: "MEDICAL CERTIFICATE - This is to certify that John Doe is unfit for work from 10/05/2023 to 17/05/2023 due to illness."
Output: {{"type": "arrêt maladie", "reasoning": "This is a medical certificate stating unfitness for work, which directly corresponds to the 'arrêt maladie' category."}}

Now, analyze this document content:

{content}

Provide your classification using the push_extracted_type function.""",
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "push_extracted_type",
                    "description": "Push extracted document type and reasoning",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "The type of document.",
                                "enum": list(valid_types.keys()),
                            },
                            "reasoning": {
                                "type": "string",
                                "description": "Explanation for the chosen document type.",
                            },
                        },
                        "required": ["type", "reasoning"],
                    },
                },
            }
        ],
    )

    # extracted_info = json.loads(
    #     response['message']['tool_calls'][0]['function']['arguments'])
    extracted_info = response["message"]["tool_calls"][0]["function"]["arguments"]

    print(
        f"{Fore.CYAN}Extracted type:{Style.RESET_ALL} {
            extracted_info['type']} ({valid_types[extracted_info['type']]})"
    )
    print(
        f"{Fore.CYAN}Reasoning:{Style.RESET_ALL} {
            extracted_info['reasoning']}"
    )
    return extracted_info


def extract_emitter(content):
    """Extracts the emitter from the document content."""
    response = ollama.chat(
        model=ollamaModel,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in document analysis, specializing in identifying the sources or creators of documents.",
            },
            {
                "role": "user",
                "content": f"""Analyze the following document content and extract the name of the person or organization who sent or created this document.

Instructions:
1. Carefully examine the document for sender information, typically found at the top or bottom of the document.
2. Look for company letterheads, logos, or official stamps that might indicate the sender.
3. Check for signatures or contact information that could reveal the emitter.
4. If the emitter is not explicitly stated, use contextual clues to make your best guess.
5. Provide a confidence level (High, Medium, Low) for your extraction.

Examples:
Input: "From: Acme Corporation\nTo: John Doe\nSubject: Invoice for Services"
Output: {{"emitter": "Acme Corporation", "confidence": "High",
    "reasoning": "Clearly stated as the sender at the beginning of the document."}}

Input: "Thank you for your purchase. If you have any questions, please contact support@techstore.com"
Output: {{"emitter": "TechStore", "confidence": "Medium",
    "reasoning": "Inferred from the support email domain, but company name not explicitly stated."}}

Now, analyze this document content:

{content}

Provide your extraction using the push_extracted_emitter function.""",
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "push_extracted_emitter",
                    "description": "Push extracted emitter, confidence, and reasoning",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "emitter": {
                                "type": "string",
                                "description": "The name of the person or organization who sent or created the document.",
                            },
                            "confidence": {
                                "type": "string",
                                "enum": ["High", "Medium", "Low"],
                                "description": "Confidence level of the extraction.",
                            },
                            "reasoning": {
                                "type": "string",
                                "description": "Explanation for the chosen emitter and confidence level.",
                            },
                        },
                        "required": ["emitter", "confidence", "reasoning"],
                    },
                },
            }
        ],
    )

    # return json.loads(response['message']['tool_calls'][0]['function']['arguments'])
    return response["message"]["tool_calls"][0]["function"]["arguments"]


def extract_recipient(content):
    """Extracts the recipient from the document content."""
    response = ollama.chat(
        model=ollamaModel,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in document analysis, specializing in identifying the intended recipients of documents.",
            },
            {
                "role": "user",
                "content": f"""Analyze the following document content and extract the name of the person or organization who received this document.

Instructions:
1. Carefully examine the document for recipient information, typically found near the top of the document.
2. Look for phrases like "To:", "Attn:", or "Dear" that often precede recipient names.
3. Check for addresses or other contact information that might indicate the recipient.
4. The recipient must be one of the following: Jérôme, Pauline, Grégoire, OLTMANNS, or WAX.
5. If the recipient is not explicitly stated, use contextual clues to determine the most likely recipient from the given list.
6. Provide a confidence level (High, Medium, Low) for your extraction.

Examples:
Input: "Dear Mr. OLTMANNS, We are pleased to inform you that your application has been accepted."
Output: {{"recipient": "OLTMANNS", "confidence": "High",
    "reasoning": "Directly addressed in the salutation of the document."}}

Input: "Invoice for services rendered to WAX Industries during Q2 2023"
Output: {{"recipient": "WAX", "confidence": "High",
    "reasoning": "WAX Industries mentioned as the client for the invoiced services."}}

Now, analyze this document content:

{content}

Provide your extraction using the push_extracted_recipient function.""",
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "push_extracted_recipient",
                    "description": "Push extracted recipient, confidence, and reasoning",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "recipient": {
                                "type": "string",
                                "description": "The name of the person or organization who received the document.",
                                "enum": [
                                    "Jérôme",
                                    "Pauline",
                                    "Grégoire",
                                    "OLTMANNS",
                                    "WAX",
                                ],
                            },
                            "confidence": {
                                "type": "string",
                                "enum": ["High", "Medium", "Low"],
                                "description": "Confidence level of the extraction.",
                            },
                            "reasoning": {
                                "type": "string",
                                "description": "Explanation for the chosen recipient and confidence level.",
                            },
                        },
                        "required": ["recipient", "confidence", "reasoning"],
                    },
                },
            }
        ],
    )

    # return json.loads(response['message']['tool_calls'][0]['function']['arguments'])
    return response["message"]["tool_calls"][0]["function"]["arguments"]


def analyze_document(content, max_retries=3):
    """
    Analyzes the document content to extract required information using the Llama model.

    :param content: The text content of the document.
    :param max_retries: Maximum number of retry attempts for each extraction (default is 3).
    :return: A dictionary containing extracted information or None if critical extractions fail.
    """
    extracted_info = {}

    # Extract subject with retry
    subject_info = retry_extraction(extract_subject, content, max_retries)
    if subject_info:
        extracted_info["subject"] = subject_info["subject"]
        print(
            f"{Fore.GREEN}Subject extracted:{
                Style.RESET_ALL} {subject_info['subject']}"
        )
        print(
            f"{Fore.CYAN}Reasoning:{Style.RESET_ALL} {
                subject_info['reasoning']}"
        )
    else:
        print(
            f"{Fore.RED}Failed to extract subject after all retries. Aborting analysis.{
                Style.RESET_ALL}"
        )
        return None

    # Extract date with retry
    date_info = retry_extraction(extract_date, content, max_retries)
    if date_info:
        extracted_info["date"] = date_info["date"]
        print(
            f"{Fore.GREEN}Date extracted:{
                Style.RESET_ALL} {date_info['date']}"
        )
        print(
            f"{Fore.CYAN}Reasoning:{Style.RESET_ALL} {
                date_info['reasoning']}"
        )
    else:
        print(
            f"{Fore.RED}Failed to extract date after all retries. Aborting analysis.{
                Style.RESET_ALL}"
        )
        return None

    # Extract type with retry
    type_info = retry_extraction(extract_type, content, max_retries)
    if type_info:
        extracted_info["type"] = type_info["type"]
    else:
        print(
            f"{Fore.RED}Failed to extract document type after all retries. Aborting analysis.{
                Style.RESET_ALL}"
        )
        return None

    # Extract emitter with retry
    emitter_info = retry_extraction(extract_emitter, content, max_retries)
    if emitter_info:
        extracted_info["emitter"] = emitter_info["emitter"]
        print(
            f"{Fore.GREEN}Emitter extracted:{
                Style.RESET_ALL} {emitter_info['emitter']}"
        )
        print(
            f"{Fore.CYAN}Confidence:{Style.RESET_ALL} {
                emitter_info['confidence']}"
        )
        print(
            f"{Fore.CYAN}Reasoning:{Style.RESET_ALL} {
                emitter_info['reasoning']}"
        )
    else:
        print(
            f"{Fore.YELLOW}Failed to extract emitter after all retries. Continuing with partial information.{
                Style.RESET_ALL}"
        )

    # Extract recipient with retry
    recipient_info = retry_extraction(extract_recipient, content, max_retries)
    if recipient_info:
        extracted_info["recipient"] = recipient_info["recipient"]
        print(
            f"{Fore.GREEN}Recipient extracted:{
                Style.RESET_ALL} {recipient_info['recipient']}"
        )
        print(
            f"{Fore.CYAN}Confidence:{Style.RESET_ALL} {
                recipient_info['confidence']}"
        )
        print(
            f"{Fore.CYAN}Reasoning:{Style.RESET_ALL} {
                recipient_info['reasoning']}"
        )
    else:
        print(
            f"{Fore.YELLOW}Failed to extract recipient after all retries. Continuing with partial information.{
                Style.RESET_ALL}"
        )

    try:
        # Validate date format
        datetime.strptime(extracted_info["date"], "%Y-%m-%d")

        # Validate document type
        if extracted_info["type"] not in valid_types:
            raise ValueError(
                f"Invalid document type: {
                    extracted_info['type']}"
            )

        print(f"{Fore.GREEN}Final extracted information:{Style.RESET_ALL}")
        for key, value in extracted_info.items():
            print(f"  {Fore.CYAN}{key}:{Style.RESET_ALL} {value}")
        return extracted_info

    except Exception as e:
        print(
            f"{Fore.RED}Error in final validation: {
                str(e)}{Style.RESET_ALL}"
        )
        return None


# Main execution
if __name__ == "__main__":
    # Example usage
    sample_content = """
    INVOICE

    Invoice Number: INV-2023-001
    Date: 15/05/2023

    From:
    TechCorp Solutions
    123 Tech Street, Silicon Valley, CA 94000

    To:
    WAX Industries
    456 Innovation Avenue, San Francisco, CA 94101

    Description                     Quantity    Unit Price    Total
    ---------------------------------------------------------------
    Software Development Services      80 hrs     $150.00    $12,000.00
    Cloud Hosting (Monthly)               1       $500.00       $500.00
    ---------------------------------------------------------------
    Subtotal                                                $12,500.00
    Tax (8.5%)                                               $1,062.50
    ---------------------------------------------------------------
    Total Due                                               $13,562.50

    Please remit payment within 30 days.
    Thank you for your business!
    """

    result = analyze_document(sample_content)
    if result:
        print(
            f"{Fore.GREEN}Document analysis completed successfully.{
                Style.RESET_ALL}"
        )
    else:
        print(f"{Fore.RED}Document analysis failed.{Style.RESET_ALL}")
