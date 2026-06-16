from cryptography.fernet import Fernet
import os

# Usar chave persistente ou gerar nova
key = os.getenv("ENCRYPTION_KEY")
if not key:
    key = Fernet.generate_key()
    # Em produção, salvar em arquivo seguro
else:
    key = key.encode()

cipher = Fernet(key)

def encrypt_data(data):
    encrypted = cipher.encrypt(data.encode())
    return encrypted

def decrypt_data(data):
    decrypted = cipher.decrypt(data)
    return decrypted.decode()