import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from dotenv import load_dotenv
import io

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

def load_decrypted_env():
    """Loads the decrypted .env file into the environment."""
    encrypted_env_path = '.env.encrypted'
    master_password = os.environ.get('SECRET_MASTER_PASSWORD')

    if not master_password:
        print("Warning: SECRET_MASTER_PASSWORD not set. Skipping decryption.")
        # Attempt to load a plaintext .env file for local development if it exists
        if os.path.exists('.env'):
            load_dotenv()
            print("Loaded secrets from plaintext .env file.")
        return

    try:
        with open(encrypted_env_path, 'rb') as f:
            salt = f.read(16)
            encrypted_data = f.read()
    except FileNotFoundError:
        raise RuntimeError(
            f"Fatal: {encrypted_env_path} not found. "
            "Please create it using the encrypt_secrets.py script."
        )

    key = generate_key_from_password(master_password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        raise RuntimeError(f"Fatal: Failed to decrypt secrets. Is the master password correct? Error: {e}")

    # Load the decrypted data as if it were a .env file
    load_dotenv(stream=io.StringIO(decrypted_data.decode()))
    print("Successfully decrypted and loaded secrets from .env.encrypted")
