# pip install py3-validate-email
from validate_email import validate_email

# Generate individual email based on a pattern
def generate_email(first, last, domain, pattern):
    return pattern.format(first, last, domain)

# Validate email domain
def is_valid_domain(email):
    try:
        return validate_email(email, verify=True)
    except:
        return False

# Generate a list of unique email variations
def generate_email_variations(first_name, last_name, company_domain):
    email_variations = set()
    patterns = [
        '{}.{}@{}',
        '{}.{}@{}',
        '{}_{}@{}',
        '{}-{}@{}',
        '{}{}@{}',
        '{}{}@{}'
    ]
    
    # Convert names to lowercase
    first_name, last_name = first_name.lower(), last_name.lower()
    
    # Create emails based on patterns
    for pattern in patterns:
        for first, last in [(first_name, last_name), (last_name, first_name),
                            (first_name[0], last_name), (first_name, last_name[0]),
                            (first_name[0], last_name), (first_name, last_name[0])]:
            email_variations.add(generate_email(first, last, company_domain, pattern))
    
    # Truncate names and generate emails
    full_name = first_name + '.' + last_name
    for i in range(len(full_name), 0, -1):
        truncated_name = full_name[:i]
        first, last = truncated_name.split('.')
        email_variations.add(generate_email(first, last, company_domain, pattern))
    
    return list(email_variations)

if __name__ == '__main__':
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    company_domain = input("Enter the company domain (e.g., gmail.com): ")
    
    email_variations = generate_email_variations(first_name, last_name, company_domain)
    
    print("\nChecking email address variations for validity...")
    for email in email_variations:
        if is_valid_domain(email):
            print(f"{email} appears to be valid.")
        else:
            print(f"{email} appears to be invalid.")