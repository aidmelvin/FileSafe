
import cryptography
from cryptography.fernet import Fernet

# generate key
key = Fernet.generate_key()
print(len(key))