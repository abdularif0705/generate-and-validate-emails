import requests
import time
import json


# Function to send a GET request to AbstractAPI for email validation
def send_email_validation_request(email_address, api_key):
    try:
        response = requests.get(
            f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email_address}"
        )
        return response.json()
    except requests.exceptions.RequestException as api_error:
        print(f"There was an error contacting the Email Validation API: {api_error}")
        return None


# Function to determine if the email is valid based on AbstractAPI response
def categorize_email(api_data):
    if api_data is None:
        return "invalid"

    general_keys = ['deliverability', 'quality_score', 'is_valid_format', 'is_free_email', 'is_disposable_email',
                    'is_role_email', 'is_catchall_email', 'is_mx_found', 'is_smtp_valid']

    if not all(key in api_data for key in general_keys):
        return "invalid"

    deliverability = api_data['deliverability']
    quality_score = float(api_data['quality_score']) # Convert to float
    is_valid_format = api_data['is_valid_format']['value']
    is_free_email = api_data['is_free_email']['value']
    is_disposable_email = api_data['is_disposable_email']['value']
    is_role_email = api_data['is_role_email']['value']
    is_catchall_email = api_data['is_catchall_email']['value']
    is_mx_found = api_data['is_mx_found']['value']
    is_smtp_valid = api_data['is_smtp_valid']['value']

    if (deliverability == "DELIVERABLE" and quality_score >= 0.95) and (
            is_valid_format and is_mx_found and is_smtp_valid):
        if not (is_free_email or is_disposable_email or is_role_email or is_catchall_email):
            return "valid"
        else:
            return "flagged"
    return "invalid"


# Generate individual email based on a pattern
def generate_email(first, last, domain, pattern):
    return pattern.format(first, last, domain)

# Generate a list of unique email variations
def generate_email_variations(first_name, last_name, company_domain):
    email_variations = set()
    patterns = [
        '{}.{}@{}',
        '{}_{}@{}',
        '{}-{}@{}',
        '{}{}@{}',
        '{}{}@{}'
    ]

    first_name, last_name = first_name.lower(), last_name.lower()

    for pattern in patterns:
        for first, last in [(first_name, last_name), (last_name, first_name),
                            (first_name[0], last_name), (first_name, last_name[0]),
                            (first_name[0], last_name[0]), (last_name[0], first_name[0])]:
            email_variations.add(generate_email(first, last, company_domain, pattern))

    return list(email_variations)

if __name__ == "__main__":
    api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key

    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    company_domain = input("Enter the company domain (e.g., gmail.com): ")

    email_variations = generate_email_variations(first_name, last_name, company_domain)

    valid_emails = []
    flagged_emails = []

    print("\nChecking email address variations for validity...")
    for email in email_variations:
        print(f"Checking {email}...")
        api_response = send_email_validation_request(email, api_key)
        print(f"API response: {api_response}")

        categorization = categorize_email(api_response)

        if categorization == "valid":
            print(f"{email} appears to be valid.")
            valid_emails.append(email)
        elif categorization == "flagged":
            print(f"{email} is flagged for review.")
            flagged_emails.append(email)
        else:
            print(f"{email} appears to be invalid.")
        time.sleep(1)  # To avoid exceeding rate limits

    print("\nValid Emails:")
    for email in valid_emails:
        print(email)

    print("\nFlagged Emails:")
    for email in flagged_emails:
        print(email)