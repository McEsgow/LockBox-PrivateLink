from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os
import subprocess
import secrets

def open_file_path(path_to_open):
    subprocess.Popen(['xdg-open', path_to_open])

def copy_file_to_clipboard(file_path):
    command = f"powershell Set-Clipboard -LiteralPath {file_path}"
    os.system(command)

def encrypt_file(file_base64, file_name, key):
    """Encrypts a file using AES encryption and the provided key."""

    if file_base64 == "":
        return "ERROR: NO FILE."
    elif key == "":
        return "ERROR: NO KEY."

    try:
        key_bytes = key.encode()
        while len(key_bytes) < 32:
            key_bytes += b'\x00'
        key_bytes = key_bytes[:32]

        # Generate a random IV
        iv = secrets.token_bytes(16)

        cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        file_data = base64.b64decode(file_base64)
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()

        new_file_name = 'LockBox/' + file_name + '.lb'
        with open(new_file_name, 'wb') as encrypted_file:
            # Prepend the IV to the ciphertext
            encrypted_file.write(iv + encrypted_data)

        copy_file_to_clipboard(os.getcwd().replace("\\", "/") + "/" + new_file_name)
        return "File Encrypted Successfully"
    except Exception as e:
        print(e)
        return "ERROR"

def decrypt_file(file_base64, file_name, key):
    """Decrypts an encrypted file using AES decryption and the provided key."""
    
    if file_base64 == "":
        return "ERROR: NO FILE."
    elif key == "":
        return "ERROR: NO KEY."

    try:
        key_bytes = key.encode()
        while len(key_bytes) < 32:
            key_bytes += b'\x00'
        key_bytes = key_bytes[:32]

        # Extract the IV from the ciphertext
        iv = base64.b64decode(file_base64)[:16]
        cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        encrypted_data = base64.b64decode(file_base64)[16:]
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        file_name = os.path.splitext(file_name)[0]
        new_file_name = 'LockBox/' + file_name

        with open(new_file_name, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)
        
        return "File Decrypted"
    except Exception as e:
        print(e)
        return "ERROR"
