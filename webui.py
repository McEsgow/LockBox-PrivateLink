#!/path/to/your/venv/bin/python

import os
import base64
import secrets

import subprocess
import platform

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from flask import Flask, render_template, request, jsonify, send_from_directory

class lockBox:
    def __init__(self) -> None:
        folder_path = 'LockBox/'
        # Check if the folder already exists
        if not os.path.exists(folder_path):
            # Create the folder if it doesn't exist
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
        else:
            print(f"Folder '{folder_path}' already exists.")
            
        pass
    def encrypt_file(self, file_base64, file_name, key):
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

            return "File Encrypted Successfully"
        except Exception as e:
            print(e)
            return "ERROR"

    def decrypt_file(self, file_base64, file_name, key):
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

    def encrypt_text(self, text, key):
        key_bytes = key.encode()
        while len(key_bytes) < 32:
            key_bytes += b'\x00'
        key_bytes = key_bytes[:32]

        # Generate a random IV
        iv = secrets.token_bytes(16)

        cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        encrypted_data = base64.b64encode(iv + encryptor.update(text.encode('utf-8')) + encryptor.finalize())
    
        return encrypted_data.decode()

    def decrypt_text(self, text, key):
        try:
            key_bytes = key.encode()
            while len(key_bytes) < 32:
                key_bytes += b'\x00'
            key_bytes = key_bytes[:32]

            # Extract the IV from the ciphertext
            iv = base64.b64decode(text)[:16]
            cipher = Cipher(algorithms.AES(key_bytes), modes.CFB(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            encrypted_data = base64.b64decode(text)[16:]
            decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

            return decrypted_data.decode()
            
        except Exception as e:
            print(e)

class privateLink:
    def generate_private_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Serialize private key to PEM format
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Encode the serialized private key to Base64
        private_key_base64 = base64.b64encode(private_key_pem).decode('utf-8')

        return private_key_base64

    def extract_public_key(self, private_key_base64):
        try:
            # Decode the Base64 private key
            private_key_pem = base64.b64decode(private_key_base64.encode('utf-8'))

            # Deserialize private key from PEM format
            private_key = serialization.load_pem_private_key(
                private_key_pem,
                password=None
            )

            # Extract the public key
            public_key = private_key.public_key()

            # Serialize public key to PEM format
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Encode the serialized public key to Base64
            public_key_base64 = base64.b64encode(public_key_pem).decode('utf-8')
        except ValueError:
            public_key_base64 = 'INVALID PRIVATE KEY!'

        return public_key_base64  

    def encrypt_key(self, public_key_base64, key_to_encrypt):
        try:
            # Decode the PEM-encoded public key from Base64
            public_key_pem = base64.b64decode(public_key_base64)

            # Load the public key from the PEM-encoded data
            public_key = serialization.load_pem_public_key(
                public_key_pem,
            )

            # Encrypt the key using the public key
            encrypted_key = public_key.encrypt(
                key_to_encrypt.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Encode the encrypted key to Base64
            encrypted_key_base64 = base64.b64encode(encrypted_key).decode()
            
            
        except:
            encrypted_key_base64 = "ERROR!"
        return encrypted_key_base64

    def decrypt_key(self, private_key_base64, encrypted_key_base64):
        try:
            # Decode the PEM-encoded private key from Base64
            private_key_pem = base64.b64decode(private_key_base64)

            # Load the private key from the PEM-encoded data
            private_key = serialization.load_pem_private_key(
                private_key_pem,
                password=None,  # No password for this example; adjust as needed
            )

            # Decode the Base64-encoded encrypted key
            encrypted_key = base64.b64decode(encrypted_key_base64)

            # Decrypt the key using the private key
            decrypted_key = private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return decrypted_key.decode('utf-8')
        except:
            return "ERROR!"

class LocalAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.route('/')(self.index)
        self.app.route('/encrypt', methods=['POST'])(self.encrypt)
        self.app.route('/decrypt', methods=['POST'])(self.decrypt)
        self.app.route('/encrypt_text', methods=['POST'])(self.encrypt_text)
        self.app.route('/decrypt_text', methods=['POST'])(self.decrypt_text)
        self.app.route('/generate_key')(self.generate_key)
        self.app.route('/generate_private_key')(self.generate_private_key)
        self.app.route('/extract_public_key', methods=['POST'])(self.extract_public_key)
        self.app.route('/decrypt_secret_key', methods=['POST'])(self.decrypt_secret_key)
        self.app.route('/encrypt_secret_key', methods=['POST'])(self.encrypt_secret_key)
        self.app.route('/open_folder')(self.open_folder)
        self.app.route('/<path:filename>')(self.serve_static)
        
        self.lock_box = lockBox()
        self.private_link = privateLink()

        if __name__ == '__main__':
            self.app.run(host="127.0.0.1", port=58538, debug=True)

    def index(self):
        return render_template('index.html')

    def open_folder(self):
        system_platform = platform.system()
        
        folder_path = r'LockBox'
        if system_platform == 'Windows':
            subprocess.Popen(['explorer', folder_path], shell=True)
        elif system_platform == 'Darwin':  # macOS
            subprocess.Popen(['open', folder_path])
        elif system_platform == 'Linux':
            subprocess.Popen(['xdg-open', folder_path])
        return jsonify({'status': 'folder opened'})

    def encrypt(self):
        base_64_file_data = request.form.get('file')
        file_name = request.form.get('filename')
        key = request.form.get('encryptionKey')
        return jsonify({'status': self.lock_box.encrypt_file(base_64_file_data, file_name, key)})

    def decrypt(self):
        base_64_file_data = request.form.get('file')
        file_name = request.form.get('filename')
        key = request.form.get('encryptionKey')
        return jsonify({'status': self.lock_box.decrypt_file(base_64_file_data, file_name, key)})

    def encrypt_text(self):
        text = request.form.get('text')
        key = request.form.get('key')
        return self.lock_box.encrypt_text(text, key)
    
    def decrypt_text(self):
        text = request.form.get('text')
        key = request.form.get('key')
        return self.lock_box.decrypt_text(text, key)

    def generate_key(self):
        return jsonify({'key': secrets.token_urlsafe(128)})

    def generate_private_key(self):
        return jsonify({'key': self.private_link.generate_private_key()})

    def extract_public_key(self):
        private_key = request.form.get('key')
        public_key = self.private_link.extract_public_key(private_key)
        return jsonify({'key': public_key})

    def decrypt_secret_key(self):
        encrypted_key = request.form.get('encrypted_key')
        private_key = request.form.get('private_key')
        decrypted_key = self.private_link.decrypt_key(private_key, encrypted_key)
        return jsonify({'key': decrypted_key})

    def encrypt_secret_key(self):
        key = request.form.get('secret_key')
        public_key = request.form.get('public_key')
        encrypted_key = self.private_link.encrypt_key(public_key, key)
        return jsonify({'key': encrypted_key})

    def serve_static(self, filename):
        return send_from_directory(os.path.join(self.app.root_path, 'static'), filename)

local_api_instance = LocalAPI()