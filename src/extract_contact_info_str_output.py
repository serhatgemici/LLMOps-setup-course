# src/extract_contact_info_correction.py
import json

import requests


def extract_contact_info(text):
    """Extract contact information using the local LLM API with structured output."""

    url = "http://localhost:8000/generate"

    # Define system prompt for role specification
    system_prompt = "You are an assistant specializing in precise data extraction. Extract only the requested information in the specified JSON format."

    # Simplified prompt since JSON schema will enforce structure
    prompt = f"Extract the contact information (name, email, phone) from the following text: {text}"

    # Define JSON schema for structured output
    contact_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "contact_extraction",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The full name of the person",
                    },
                    "email": {
                        "type": "string",
                        "description": "The email address of the person",
                    },
                    "phone": {
                        "type": "string",
                        "description": "The phone number of the person",
                    },
                },
                "required": ["name", "email", "phone"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }

    # Set parameters - low temperature for deterministic extraction
    payload = {
        "prompt": prompt,
        "system_prompt": system_prompt,
        "model": "openai/gpt-oss-120b",
        "temperature": 0.1,  # Low temperature for consistent data extraction
        "max_tokens": 150,
        "response_format": contact_schema,  # Enable structured output
    }

    # Make the API call
    response = requests.post(url, json=payload)
    response_data = response.json()

    # Parse the response string as JSON
    try:
        extracted_info = json.loads(response_data["response"])
        return extracted_info
    except json.JSONDecodeError:
        # Return a structured error if parsing fails
        return {
            "error": "Failed to parse response as JSON",
            "raw_response": response_data["response"],
        }


if __name__ == "__main__":
    # Test with example text
    test_text = "Contact our project manager Marc Dubois at 06-12-34-56-78 or marc.dubois@company.com"
    result = extract_contact_info(test_text)

    print("Input text:", test_text)
    print("\nExtraction result:")
    print(json.dumps(result, indent=2))

    # Expected output:
    # {"name": "Marc Dubois", "email": "marc.dubois@company.com", "phone": "06-12-34-56-78"}
