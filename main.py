from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Serialize private and public keys to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Encode the serialized keys to Base64
    private_key_base64 = base64.b64encode(private_key_pem).decode('utf-8')
    public_key_base64 = base64.b64encode(public_key_pem).decode('utf-8')

    return private_key_base64, public_key_base64

def encrypt_key(public_key_base64, key_to_encrypt):
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
    
    return encrypted_key_base64

def decrypt_key(private_key_base64, encrypted_key_base64):
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

