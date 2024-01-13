from flask import Flask, render_template, request, jsonify, send_from_directory
import os


import secrets
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

import private_link
import lock_box


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    base_64_file_data = request.form.get('file')
    file_name = request.form.get('filename')
    key = request.form.get('encryptionKey')
    return jsonify({'status': lock_box.encrypt_file(base_64_file_data, file_name, key)})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    base_64_file_data = request.form.get('file')
    file_name = request.form.get('filename')
    key = request.form.get('encryptionKey')
    return jsonify({'status': lock_box.decrypt_file(base_64_file_data, file_name, key)})

@app.route('/generate_key')
def generate_key():
    return jsonify({'key': secrets.token_urlsafe(128)})

@app.route('/generate_private_key')
def generate_private_key():
    return jsonify({'key': private_link.generate_private_key()})

@app.route('/extract_public_key', methods=['POST'])
def extract_public_key():
    # Get the private key from the POST data
    private_key = request.form.get('key')

    public_key = private_link.extract_public_key(private_key)

    # Return the public key as a JSON response
    return jsonify({'key': public_key})

@app.route('/decrypt_secret_key', methods=['POST'])
def decrypt_secret_key():
    # Get the private key from the POST data
    encrypted_key = request.form.get('encrypted_key')
    private_key = request.form.get('private_key')
    decrypted_key = private_link.decrypt_key(private_key, encrypted_key)

    # Return the public key as a JSON response
    return jsonify({'key': decrypted_key})

@app.route('/encrypt_secret_key', methods=['POST'])
def encrypt_secret_key():
    # Get the private key from the POST data
    key = request.form.get('secret_key')
    public_key = request.form.get('public_key')
    encrypted_key = private_link.encrypt_key(public_key, key)
    # Return the public key as a JSON response
    return jsonify({'key': encrypted_key})

# Define a route to serve static files (like app.js)
@app.route('/static/<path:filename>')
def serve_static(filename):
    
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':

    app.run(debug=True)
