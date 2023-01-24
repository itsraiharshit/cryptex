import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

SALT = b'\xfa\xda\x1d\x7c\xab\x15\xdb\xd8\x2d\x15\x17\x72\x8a\x4a\xba\x3f'

def generate_key(password):
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt(password, file_in, file_out):
    key = generate_key(password)
    f = Fernet(key)
    with open(file_in, 'rb') as f_in:
        data = f_in.read()
    encrypted_data = f.encrypt(data)
    with open(file_out, 'wb') as f_out:
        f_out.write(encrypted_data)

def decrypt(password, file_in, file_out):
    key = generate_key(password)
    f = Fernet(key)
    with open(file_in, 'rb') as f_in:
        data = f_in.read()
    decrypted_data = f.decrypt(data)
    with open(file_out, 'wb') as f_out:
        f_out.write(decrypted_data)

while True:
    print('''
    1. Encrypt
    2. Decrypt
    3. Exit
    ''')
    user_choice = input("Enter your choice: ")

    if "3" in user_choice:
        exit()
    elif "1" in user_choice:
        print("Encryption")
        print("make sure the file is in same directory")
        originalfilename = input("Enter file name: ")
        encryptedfilename = input("Enter the name you want to give your encrypted file: ")
        password = input("Enter the Password: ")
        encrypt(password, originalfilename, encryptedfilename)
        print("Encryption Done")
    elif "2" in user_choice:
        print("Decryption")
        originalfilename = input("Enter file name: ")
        decryptedfilename = input("Enter the name you want to give your decrypted file: ")
        password = input("Enter the Password: ")
        decrypt(password, originalfilename, decryptedfilename)
    else:
        print("Please enter a Valid Option")

