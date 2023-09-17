import json
import requests
import time

# Function to send a GET request to AbstractAPI for email validation
def send_email_validation_request(email_address, api_key):
    try:
        response = requests.get(
            f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email_address={email_address}"
        )
        return response.json()
    except requests.exceptions.RequestException as api_error:
        print(f"There was an error contacting the Email Validation API: {api_error}")
        return None

# Function to determine if the email is valid based on AbstractAPI response
def is_valid_email(api_data):
    if api_data is None:
        return False

    is_valid_format = api_data.get('is_valid_format', {}).get('value', False)
    is_free_email = api_data.get('is_free_email', {}).get('value', False)
    is_disposable_email = api_data.get('is_disposable_email', {}).get('value', False)
    is_role_email = api_data.get('is_role_email', {}).get('value', False)
    is_catchall_email = api_data.get('is_catchall_email', {}).get('value', False)
    is_mx_found = api_data.get('is_mx_found', {}).get('value', False)
    is_smtp_valid = api_data.get('is_smtp_valid', {}).get('value', False)

    if (is_valid_format and is_mx_found and is_smtp_valid and
        not (is_free_email or is_disposable_email or is_role_email or is_catchall_email)):
        return True

    return False

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


# Main code block
if __name__ == "__main__":
    api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key

    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    company_domain = input("Enter the company domain (e.g., gmail.com): ")

    email_variations = generate_email_variations(first_name, last_name, company_domain)

    print("\nChecking email address variations for validity...")
    valid_emails = []
    for email in email_variations:
        api_response = send_email_validation_request(email, api_key)
        if is_valid_email(api_response):
            valid_emails.append(email)

        time.sleep(1)  # Sleep for 1 second to avoid exceeding the rate limit

    if valid_emails:
        print("\nThe following email addresses appear to be valid:")
        for email in valid_emails:
            print(email)
    else:
        print("\nNo valid email addresses found.")