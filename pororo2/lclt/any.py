import secrets
import string

def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(letters) for _ in range(length))