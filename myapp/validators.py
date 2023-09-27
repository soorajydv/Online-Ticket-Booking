import re

def is_valid_password(password):
    # Check if the password is at least 8 characters long
    if len(password) < 8:
        return False, "Your password must contain at least 8 characters."

    # Check if the password contains only letters, digits, @/./+/-/_
    if not re.match(r'^[A-Za-z0-9@/./+/-/_]+$', password):
        return False, "Your password can only contain letters, digits, @/./+/-/_."

    # Check if the password is not entirely numeric
    if password.isnumeric():
        return False, "Your password can't be entirely numeric."

    # Check if the password is not too similar to personal information (you can extend this logic)
    personal_info = ['username', 'first_name', 'last_name', 'email', 'phone']
    for info in personal_info:
        if info.lower() in password.lower():
            return False, "Your password can't be too similar to your personal information."

    # Check if the password is not a commonly used password (you can add more common passwords)
    common_passwords = ['password123', 'qwerty', '123456']
    if password in common_passwords:
        return False, "Your password can't be a commonly used password."

    # If all checks pass, the password is valid
    return True, "Password is valid."

# Test the password validation function
# password = input("Enter your password: ")
# valid, message = is_valid_password(password)



def is_valid_email(email):
    # Define a regular expression pattern for a valid email address
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Use re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False

# Test the email validation function
# email = input("Enter an email address: ")
# if is_valid_email(email):
#     print("Valid email address.")
# else:
#     print("Invalid email address.")
