from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import requests

message = "Alô, mundo!"
message2 = "!odnum, ôlA"
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

receiver_pk_response = requests.get('http://flask:5000/public-key').text.encode()
receiver_public_key = serialization.load_pem_public_key(receiver_pk_response)

# Encrypts the message using the public key from the receiver.
encrypted_message = receiver_public_key.encrypt(message.encode('utf8'),
                                                padding.OAEP(
                                                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                    algorithm=hashes.SHA256(),
                                                    label=None
                                                ))

encrypted_message2 = receiver_public_key.encrypt(message2.encode('utf8'),
                                                 padding.OAEP(
                                                     mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                     algorithm=hashes.SHA256(),
                                                     label=None
                                                 ))

# Creates a signature using the sender's private key
signature = private_key.sign(encrypted_message,
                             padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                         salt_length=padding.PSS.MAX_LENGTH),
                             hashes.SHA256())

# Sends the message and the signature to AppB
print("Sending the message with the correct signature...")
requests.post('http://flask:5000', json={'encrypted_message': encrypted_message.hex(),
                                         'signature': signature.hex(),
                                         'public_key': public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                                               format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()})
print("Sending a different message with the previous signature...")
requests.post('http://flask:5000', json={'encrypted_message': encrypted_message2.hex(),
                                         'signature': signature.hex(),
                                         'public_key': public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                                               format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()})
