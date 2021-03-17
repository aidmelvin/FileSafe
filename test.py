
import cryptography
from cryptography.fernet import Fernet

# generate key
key = Fernet.generate_key()

# write key to external file for saving
with open('mykey.key', 'wb') as mykey:
    mykey.write(key)

with open('mykey.key', 'rb') as mykey:
    key = mykey.read()

# creates a Fernet object
f = Fernet(key)


print('original key:', str(key))
password = 'hello'
new_key = bytes(password, 'utf-8') + key[len(password):]
print('new key:\t ', str(new_key))



# # opens file to be encrypted
with open('good_stocks.rtf', 'rb') as original_file:
    original = original_file.read()

# # encrypts file
encrypted = f.encrypt(original)

# writes encrypted data to external file
with open('encrypted_stocks.rtf', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

# decrypted = f.decrypt(encrypted)

# with open('recovered_stocks.rtf', 'wb') as decrypted_file:
#     decrypted_file.write(decrypted)

