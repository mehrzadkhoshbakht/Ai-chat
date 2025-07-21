import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def generate_key_from_password(password, salt):
    """Generates a key from a password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_env_file():
    """Encrypts the .env file."""
    try:
        with open('.env', 'rb') as f:
            plaintext = f.read()
    except FileNotFoundError:
        print("Error: .env file not found. Please create it first.")
        return

    password = getpass.getpass("Enter a master password for encryption: ")

    # Generate a random salt
    salt = os.urandom(16)

    # Derive a key from the password
    key = generate_key_from_password(password, salt)
    fernet = Fernet(key)

    # Encrypt the data
    encrypted_data = fernet.encrypt(plaintext)

    # Save the salt and encrypted data to a file
    with open('.env.encrypted', 'wb') as f:
        f.write(salt)
        f.write(encrypted_data)

    print("Successfully encrypted .env to .env.encrypted")
    print("IMPORTANT: Store your master password safely. It is required to run the application.")

if __name__ == "__main__":
    encrypt_env_file()
