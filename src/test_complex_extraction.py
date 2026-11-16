from extract_contact_info_str_output import extract_contact_info
import json


def test_complex_cases():
    # Defines a list of 5 complex test cases with different formats:
    # Titles (Dr., Mrs., Mr.)
    # Compound names (Jean-Baptiste, Marie-Claire)
    # Varied phone formats (with dots, spaces, dashes)
    # Emails with different domains

    test_cases = [
        "For any questions, contact Dr. Marie-Claire Dupont at m.dupont@hospital.fr or at +33-1-42-86-75-30",
        "Jean-Baptiste de la Fontaine (jb.fontaine@company.org) - Tel: 07.89.12.34.56",
        "Ms. Sophie MARTIN, HR manager (sophie.martin@entreprise.com, 06 12 34 56 78)",
        "Contact: Pierre Durand - Email: pierre@startup.io - Mobile: 0612345678",
        "Call Mr. Alexandre Petit at the number 01 23 45 67 89 or write to a.petit@corp.fr",
    ]

    # For each test case:
    # Display the input text
    # Call extract_contact_info()
    # Display the result formatted in JSON
    # Validate that the structure contains the 3 required fields
    # Display ✅ or ❌ based on the validation

    for i, test_case in enumerate(test_cases, 1):
        result = extract_contact_info(test_case)
        print(f"Test case {i}:")
        print("Input text:", test_case)
        print("Extraction result:")
        print(json.dumps(result, indent=2))
        # Validate that the structure contains the 3 required fields
        if isinstance(result, dict) and all(
            key in result for key in ["name", "email", "phone"]
        ):
            print("✅ Valid Structure")
        else:
            print("❌ Invalid Structure")
        print()


if __name__ == "__main__":
    test_complex_cases()
