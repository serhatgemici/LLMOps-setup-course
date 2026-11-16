import requests
import json


def extract_contact_info(text):
    """Extract contact information using the local LLM API."""

    url = "http://localhost:8000/generate"

    # Define system prompt for role specification
    system_prompt = "You are an assistant specialized in precise data extraction. Extract only the requested information in the specified JSON format. Do not make any comments."

    # Create few-shot examples in the prompt
    prompt = f"""Extract the name, email, and phone number from the following text and return them in JSON format.

Examples:
 "Please contact Jean Martin at jean.martin@example.com or at 01-23-45-67-89" → {{"name": "Jean Martin", "email": "jean.martin@example.com", "phone": "01-23-45-67-89"}}
 "For more information: Sophie Durand (sophie@company.fr, 07-11-22-33-44)" → {{"name": "Sophie Durand", "email": "sophie@company.fr", "phone": "07-11-22-33-44"}}
 "Our representative Pierre Blanc (p.blanc@corp.com) can be reached at 06-99-88-77-66" → {{"name": "Pierre Blanc", "email": "p.blanc@corp.com", "phone": "06-99-88-77-66"}}

Now:
"{text}" → """

    # Set parameters - low temperature for deterministic extraction
    payload = {
        "prompt": prompt,
        "system_prompt": system_prompt,
        "model": "openai/gpt-oss-120b",
        "temperature": 0.1,  # Low temperature for consistent data extraction
        "max_tokens": 150,
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
